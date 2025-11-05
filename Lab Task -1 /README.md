# 🧑‍💻 CSE-478: Introduction to Computer Security Lab  
## 🔹 Lab 1 — Basic Linux Familiarity

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

### 🧠 Sample Exercises

 Exercise 1 — Using Man Pages
bash
man ls
man chmod
Describe the purpose of each command and list key options.

Exercise 2 — File System Navigation
bash
Copy code
pwd
cd /usr/bin
ls -l
List directory contents and identify file permissions.

Exercise 3 — File Permissions
bash
Copy code
chmod 764 file.txt
ls -l file.txt
Explain what the numeric mode 764 represents.

Exercise 4 — Symbolic Links
bash
Copy code
ln -s /etc/init.d/myservice /etc/rc2.d/S98myservice
ls -l
Create a symbolic link and verify it using ls -l.

Exercise 5 — Environment Variables
bash
Copy code
echo $HOME
echo $PATH
export PATH=/data/course/bin:$PATH
Document the change in the environment variable and explain its impact.
