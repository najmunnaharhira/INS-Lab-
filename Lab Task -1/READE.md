# 🧑‍💻 CSE-478: Introduction to Computer Security Lab  
## 🔹 Lab 1 — Basic Linux Familiarity

---

### 🎯 Objective
The objective of this lab is to gain familiarity with the **Linux operating system**, its **command-line interface**, and **file-system structure**.  
This foundational knowledge enables effective system-level operations and prepares students for working in Unix-like environments in subsequent labs.

---

### 📘 Introduction
This lab introduces the fundamentals of **Linux and UNIX**.  
Students will explore the history of UNIX, identify major Linux distributions, and learn how to use terminal commands for file manipulation, permissions, and process management.

Through this lab, students will gain hands-on experience with:

- The **Terminal and Shell (Bash)**
- **File-system hierarchy**
- **File and directory permissions**
- **Manual (man) pages and system documentation**
- **Redirection, piping, and environment variables**

---

### 🧩 Topics Covered

1. **Linux Basics**
   - Introduction to UNIX & Linux  
   - Overview of distributions (Ubuntu, Fedora, Debian, etc.)  
   - Graphical vs Command-line interfaces  

2. **The Terminal**
   - Using the shell (`bash`)  
   - Basic commands:  
     `ls`, `cd`, `pwd`, `cat`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`  
   - Understanding the command prompt  

3. **Manual Pages**
   - Accessing help with `man`  
   - Navigating sections and syntax  
   - Practical examples:  
     ```bash
     man man
     man ls
     man chmod
     ```

4. **Linux File System**
   - Directory structure: `/`, `/home`, `/etc`, `/usr`, `/tmp`, `/var`  
   - Absolute vs Relative paths  
   - Directory navigation techniques  

5. **File Permissions**
   - Understanding read (`r`), write (`w`), and execute (`x`) permissions  
   - Commands: `chmod`, `chown`, `chgrp`  
   - Numeric and symbolic permission modes  

6. **Symbolic Links**
   - Creating and managing symbolic links using `ln -s`  

7. **Shell Operations**
   - Command history, editing, and tab completion  
   - Managing environment variables (`PATH`, `HOME`, etc.)  
   - Exporting and modifying variables  

8. **Redirection and Pipes**
   - Input/output redirection (`>`, `>>`, `<`)  
   - Piping commands (`|`)  
   - Handling `stdout` and `stderr` (`2>&1`)  

9. **Processes and Jobs**
   - Managing background and foreground processes  
   - Monitoring active processes using `ps`, `top`, `kill`  

---

## 🧠 Lab Exercises

### 🧩 Exercise 1 — Using Man Pages
**Goal:** Learn how to access Linux manual pages and understand command usage.

```bash
man ls
man chmod
Task:

Describe the purpose of each command.

List at least three options for each command (e.g., -l, -a, -R for ls).

Write a short summary of how man helps users in Linux.

🧩 Exercise 2 — File System Navigation
Goal: Explore the Linux file system and understand directory structure.

bash
pwd
cd /usr/bin
ls -l
Task:

Identify the absolute path of your current directory.

List directory contents with details and explain the permission columns.

Note differences between absolute and relative paths.

🧩 Exercise 3 — File Permissions
Goal: Learn to modify and verify file permissions.

bash
chmod 764 file.txt
ls -l file.txt
Task:

Explain what the numeric mode 764 represents.

Compare symbolic and numeric permission modes.

Show the difference before and after running the command.

🧩 Exercise 4 — Symbolic Links
Goal: Create and manage symbolic links.

bash
ln -s /etc/init.d/myservice /etc/rc2.d/S98myservice
ls -l
Task:

Create a symbolic link and verify it.

Explain the difference between hard links and symbolic links.

🧩 Exercise 5 — Environment Variables
Goal: Understand and manipulate environment variables.

bash
echo $HOME
echo $PATH
export PATH=/data/course/bin:$PATH
Task:

Display the values of HOME and PATH.

Explain what the export command does.

Document the change and its effect on the system.

🧩 Exercise 6 — Redirection and Piping
Goal: Learn to redirect outputs and chain commands.

bash
ls -l > output.txt
cat output.txt | grep ".txt"
echo "This is a test" >> output.txt
cat output.txt
Task:

Redirect command outputs to files.

Use pipes (|) to filter text.

Demonstrate appending to a file and explain the difference between > and >>.

🧩 Exercise 7 — Process Management
Goal: Learn to manage active and background processes.

bash
ps
top
sleep 100 &
jobs
kill <PID>
Task:

Display the list of running processes.

Identify the PID of your background job.

Terminate the process using kill.

Explain the difference between foreground and background jobs.
