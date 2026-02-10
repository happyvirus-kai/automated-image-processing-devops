import os

def test_output_folder_exists():
    assert os.path.exists("output_images")

def test_images_processed():
    files = os.listdir("put_images")
    assert len(files) > 0