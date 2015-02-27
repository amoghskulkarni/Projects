#!/usr/bin/python
# Author: Pranav Srinivas Kumar
# Date: 2015.02.27

import os, sys, subprocess, getopt

# ROS Indigo Installer class
# 
# Installs ROS Indigo from source at the provided path
# Usage: sudo ./
class ROS_Indigo_Installer():
    # Initialize Installer
    def __init__(self, argv):
        self.path = ""
        self.args = argv

        # Print colors
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'

    # Usage Print
    def usage(self):
        print "INSTALLER::" + self.FAIL + self.BOLD + "ERROR" + self.ENDC + "::Usage Error!"
        print "INSTALLER::USAGE::\"sudo ./setup_ros.py --path <absolute_path>\""

    # Ensure sudo
    def check_sudo(self):
        user = os.getenv("USER")
        sudo_user = os.getenv("SUDO_USER")
        if user != "root" and sudo_user == None:
            print "INSTALLER::Please run this script as root!"
            self.usage()
            sys.exit(2)
        
    # Get absolute path where ROS-Indigo will be setup
    def get_path(self):
        try:
            opts, args = getopt.getopt(self.args, "p:v", ["path="])
        except getopt.GetoptError:
            self.usage()
            sys.exit(2)

        if opts == []:
            self.usage()
            sys.exit(2)
        else:
            for option, value in opts:
                if option == "--path":
                    self.path = value
                else:
                    self.usage()

    # Ask the user a question
    def ask(self, question):

        # Define the valid answers
        valid = {"yes": True, "no": False}
        prompt = " [yes/no] "

        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if choice in valid:
                return valid[choice]
            else:
                print "INSTALLER::Please Respond with a 'yes' or 'no'"

    # Create the ROS Indigo Source Directory
    def create_source_dir(self):
        self.HOME = os.path.join(self.path, "ROS-Indigo")
        print "INSTALLER::" + self.WARNING + "ROS Source Path will be: " + self.HOME + self.ENDC 
        if self.ask("INSTALLER::Proceed with Installation?"):
            if not os.path.exists(self.HOME):
                os.makedirs(self.HOME)
                print "INSTALLER::Created Directory: " + self.HOME
            else:
                print "INSTALLER::Found Existing Directory: " + self.HOME
        else:
            print "INSTALLER::Installation Aborted!"
            sys.exit(2)

    # Setup sources list
    def setup_sources_list(self):
        os.chdir(self.HOME)
        with open("/etc/apt/sources.list.d/ros-latest.list", 
                  "w") as sources:
            sources.write("deb http://packages.ros.org/ros/ubuntu trusty main\n")
            sources.close()
            
    # Setup keys
    def setup_keys(self):
        os.chdir(self.HOME)
        p1 = subprocess.Popen(["wget", 
                               "https://raw.githubusercontent.com/ros/rosdistro/master/ros.key",
                               '-O', '-'],
                               stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["apt-key", 
                               "add", 
                               "-"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output, err = p2.communicate()

    # Install Bootstrap Dependencies
    def install_bootstrap_dependencies(self):
        os.chdir(self.HOME)
        p = subprocess.Popen(['apt-get', 
                              'install', 
                              'python-rosdep',
                              'python-rosinstall-generator', 
                              'python-wstool', 
                              'python-rosinstall', 
                              'build-essential'])
        p.wait()

    # Run the installer
    def run(self):
        # Check for sudo
        self.check_sudo()
        # Get absolute path to installation
        self.get_path()
        # Create Directory
        self.create_source_dir()
        # Setup sources list
        self.setup_sources_list()
        # Setup keys
        self.setup_keys()
        # Install Bootstrap Dependencies
        self.install_bootstrap_dependencies()

if __name__ == "__main__":

    # Instantiate a ROS Installer Object
    Installer = ROS_Indigo_Installer(sys.argv[1:])
    # Run the installer
    Installer.run()

