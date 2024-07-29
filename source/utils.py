import os 

# Function to resolve the absolute path to a file
def resolve_path_to_file(relative_path):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    absolute_path = os.path.abspath(os.path.join(script_dir, relative_path))
    
    return absolute_path