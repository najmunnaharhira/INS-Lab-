# 🧑‍💻 CSE-478: Introduction to Computer Security Lab  
## 🔹 Lab 1 — Basic Linux Familiarity

### 🎯 **Objective**
The objective of this lab is to get familiar with the **Linux operating system**, its **command-line interface**, and **file system structure**.  
This knowledge is foundational for performing system-level operations and working with Unix-like environments in future labs.

---

### 📘 **Introduction**
This lab introduces students to **Linux and UNIX fundamentals**.  
You’ll explore the history of UNIX, understand the Linux distributions, and learn how to use commands in the terminal for file manipulation, permissions, and process handling.

You will also gain hands-on experience with:
- The **Terminal & Shell (bash)**
- **File system hierarchy**
- **File and directory permissions**
- **Man pages and documentation**
- **Redirection, piping, and environment variables**

---

### 🧩 **Topics Covered**

1. **Linux Basics**
   - Introduction to UNIX & Linux
   - Understanding distributions (Ubuntu, Fedora, etc.)
   - GUI and Command-line interfaces

2. **The Terminal**
   - Using the shell (`bash`)
   - Basic commands (`ls`, `cd`, `pwd`, `cat`, `cp`, `mv`, `rm`, `mkdir`, etc.)
   - Understanding the command prompt

3. **Man Pages**
   - Using the `man` command
   - Exploring sections and syntax
   - Practical: `man man`, `man ls`, `man chmod`

4. **Linux File System**
   - Structure (`/`, `/home`, `/etc`, `/usr`, `/tmp`, etc.)
   - Absolute vs Relative Paths
   - Navigating directories

5. **File Permissions**
   - Understanding `r`, `w`, `x` permissions
   - Using `chmod`, `chown`, `chgrp`
   - Numeric and symbolic modes

6. **Symbolic Links**
   - Creating and managing symbolic links with `ln -s`

7. **Shell Operations**
   - Command history, editing, tab completion
   - Environment variables (`PATH`, `HOME`, etc.)
   - Exporting and manipulating variables

8. **Redirection and Pipes**
   - Input/output redirection (`>`, `>>`, `<`)
   - Piping commands (`|`)
   - Handling stdout and stderr (`2>&1`)

9. **Processes and Jobs**
   - Understanding process management
   - Running background and foreground jobs

---

### 🧠 **Sample Exercises**

#### **Exercise 1: Using Man Pages**
```bash
man ls
man chmod
