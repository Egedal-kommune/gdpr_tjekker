from pathlib import Path

class GdprTjekker:

    def __init__(self, path):
        self.p = Path(path)

    def get_filepaths(self, extension, search_string):
        results = []
        all_files = list(self.p.rglob(f'*.{extension}')) 

        for file in all_files:
            if search_string in file.name.lower():
                results.append(file)
        
        return results

    def delete_files(self, filepath):
        filepath.unlink()