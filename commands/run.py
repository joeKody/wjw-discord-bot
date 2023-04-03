import discord
from discord.ext import commands
from sys import platform
import os
import subprocess
import time
import threading

#import psutil

"""
def find_a(exe: str, return_arr):
    found = false;
    while not found:
        if return_arr[1] < 0:
            return
        for process in psutil.process_iter():
            if process.name() == exe:
                a_proc = process;
                found = True;
                break;
    a_proc_mem = a_proc.memory_full_info().uss;
    return_arr[0] = a_proc_mem;
    return
"""

def write_from_source(language:str, source:str):
    source_file = os.path.join(os.getcwd(), "compiled", "source.{0}".format(language));
    try:
        with open(source_file, 'w', encoding='utf-8') as f:
            f.write(source);
            f.close();
            return 0;
    except:
        return -1;

def compile_from_file(source):
    pass

def run_from_exe(source):
    pass

@commands.command()
async def run(ctx, language: str, *, code=None):
    output = discord.Embed();
    python = ["py", "python"];
    clang = ["c", "c++", "cpp"];
    in_cpp = language in clang;
    in_py = language in python;
    if (not in_cpp and not in_py):
        output.title = "Writing source failed";
        output.color = discord.Color.red();
        output.add_field(name="Reason :", value="Please specify a supported language");
        await ctx.send(embed=output);
        return -1

    # Strip everything other than the source code
    source = ctx.message.content[5:]
    source = source[len(language)+1:];
    first_tilde = source[:3];
    if (first_tilde == "```"):
        source = source[3:-4];
        char_index = 0;
        while (source[char_index] != "\n"):
            char_index = char_index + 1;
        else:
            source = source[char_index:];
    else:
        while source[0] == "\n":
            source = source[1:];

    # Check for sus codes and set language = filetype
    # I (Joe) run the code on termux, and it doesnt support gcc
    # but my pc does, so it is this way, yeah
    if (in_py):
        compiler = "python3"
        language = "py";
        sus_list = ["import os", "from os", "from pathlib", "import path", "import sys", "from sys"];
        for sus in sus_list:
            if sus in source:
                output.title = "Writing source failed";
                output.color = discord.Color.red();
                output.add_field(name="Reason :",value="Risky libraries are not allowed");
                await ctx.send(embed=output);
                return -1;

    elif (in_cpp):
        if (language == "c"):
            language = "c";
            if platform == "win32":
                compiler = "gcc";
            else:
                compiler = "clang";
        else:
            language = "cpp";
            if platform == "win32":
                compiler = "g++";
            else:
                compiler = "clang++";

    write_src_error = write_from_source(language, source);
    if (write_src_error == -1):
        output.title = "Writing source failed";
        output.color = discord.Color.dark_red();
        output.description = "Something unknown went wrong!";
        await ctx.send(embed=output);
        return -1;

    try:
        if platform == "win32":
            file = "a.exe";
        else:
            file = "a.out";
        os.remove(file);
    except:
        pass

    # compilation and running
    try:
        prev_time = time.time();
        source_file = os.path.join(os.getcwd(), "compiled", "source.{0}".format(language));
        compile_process = subprocess.run([compiler, source_file], stderr=subprocess.PIPE, text=True, timeout=15, stdout=subprocess.PIPE);
        compile_time = time.time() - prev_time;
        if (compile_process.returncode != 0):
            error = discord.Embed();
            error.title = "Compilation not successful";
            error.set_footer(text=f"Compile time : {compile_time}s");
            error.color = discord.Color.red();
            error.add_field(name="stderr :", value=f"```{compile_process.stderr} ```");
            stdout = compile_process.stdout;
            if stdout != None:
                error.add_field(name="stdout :", value=f"```{compile_process.stderr} ```");
            await ctx.send(embed=error);
        else:
            # Python is interpreted
            if language == "py":
                output.title = "Running completed";
                output.color = discord.Color.green();
                output.add_field(name="Output:", value=f"```{compile_process.stdout} ```");
                output.set_footer(text=f"Runtime : {compile_time}s\nMemory : KB");
                await ctx.send(embed=output);
                return 0;

            output.title = "Compilation completed";
            if platform == "win32":
                file = "a.exe";
                command = ".\\" + file;
            else:
                file = "a.out";
                command = "./" + file;
            memory = [0, 1];
            #pid = threading.Thread(target=find_a, args=[file, memory],daemon=True);
            try:
                #pid.start();
                prev_time = time.time();
                run_process = subprocess.run(command, stderr=subprocess.PIPE, text=True, timeout=45, stdout=subprocess.PIPE);
                run_time = time.time() - prev_time;
                # thread should stop
                memory[1] = -1;
                if (run_process.returncode != 0):
                    warning = discord.Embed();
                    warning.title = "Compilation completed";
                    warning.color = discord.Color.light_gray();
                    warning.description = f"Error while running : returncode ({run_process.returncode})";
                    warning.add_field(name="stderr :",value=f"```{run_process.stderr} ```");
                    warning.add_field(name="stdout :", value=f"```{run_process.stdout} ```");
                    warning.set_footer(text=f"Compile time : {compile_time}s\nRuntime : {run_time}s");
                    await ctx.send(embed=warning);
                else:
                    output.description = "Running completed";
                    output.color = discord.Color.green();
                    output.add_field(name="Output :",value=f"```{run_process.stdout} ```");
                    if memory[0] == 0:
                        membytes = "-";
                    else:
                        membytes = memory[0];
                    output.set_footer(text=f"Compile time : {compile_time}s\nRuntime : {run_time}s\nMemory : {membytes} bytes");
                    await ctx.send(embed=output);
                return 0;

            except subprocess.TimeoutExpired as e:
                error = discord.Embed();
                error.title = "Running failed!";
                error.color = discord.Color.red();
                error.add_field(name="Reason :", value="Runtime took to long! The limit is 45 seconds!");
                await ctx.send(embed=error);
                return -1;
            except Exception as e:
                error_str = str(e);
                error = discord.Embed();
                error.title = "Running failed!";
                error.add_field(name="Reason :", value=f"```{error_str} ```");
                error.color = discord.Color.red();
                await ctx.send(embed=error);
                return -1;

    except subprocess.TimeoutExpired as e:
        error = discord.Embed();
        error.title = "Compilation failed";
        error.color = discord.Color.red();
        error.add_field(name="Reason :", value="Compilation took to long! The limit is 15 seconds!");
        await ctx.send(embed=error);
    except Exception as e:
        error = discord.Embed();
        error.title = "Compilation failed";
        error_str = str(e);
        error.color = discord.Color.red();
        error.add_field(name="Reason :", value=f"```{error_str} ```");
        await ctx.send(embed=error);
    finally:
        return -1;

@run.error
async def run_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        output = discord.Embed(title="Command Error", description="Wrong arguments, to run code, type `;run <language> <code>`", color=discord.Color.red());
        await ctx.send(embed=output);
        return
    print(error);

def setup(bot):
  bot.add_command(run);
