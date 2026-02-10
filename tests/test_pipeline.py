import os

def test_output_folder_exists():
    assert os.path.exists("output")

def test_images_processed():
    files = os.listdir("input")
    assert len(files) > 0