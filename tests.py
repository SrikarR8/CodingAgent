from functions.get_files_info import get_files_info
from functions.get_file_contents import get_file_content
from functions.run_python_file import run_python_file

def main():
    
    working_dir = "calculator"
    #Tests for getFilesInfo:
    # print(get_files_info(working_dir))
    # print(get_files_info(working_dir, "pkg"))
    # print(get_files_info(working_dir, "/bin"))
    #print(get_files_info(working_dir, "../"))

    #Tests for get_files_content
    # print(get_file_content(working_dir,"main.py"))
    # print(get_file_content(working_dir, "pkg/calculator.py"))
    # print(get_file_content(working_dir, "/pkg/notexists.py"))
    # print(get_file_content(working_dir, "bin/cat"))

    #Tests for running python file

    print(run_python_file(working_dir, "main.py", ["3 + 5"]))

main()