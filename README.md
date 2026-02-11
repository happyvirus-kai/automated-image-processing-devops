Automated Image Processing using DevOps CI Pipeline

📌 Project Overview

This project implements an automated image processing pipeline using Python and OpenCV, integrated with DevOps practices such as version control, automated testing, and Continuous Integration (CI).

The system processes images automatically, applies multiple visual effects, and validates outputs through tests executed in a CI pipeline. This project was developed as part of a DevOps midterm activity to demonstrate both software automation and image processing fundamentals.

Implemented Image Effects:

🎨 Color Pop Effect

⚡ Neon Glow Effect

🌧️ Rain / Snow Effect

😷 Face Mask Detection

🛠️ Technologies Used:

Python 3

OpenCV

NumPy

Git & GitHub

GitHub Actions (CI)

Visual Studio Code

📁 Project Structure
.

├── src/

│   ├── main.py

│   ├── color_pop.py

│   ├── neon.py

│   ├── rain_snow.py

│   └── face_mask.py

├── tests/

│   ├── test_pipeline.py

├── input/

├── output/

├── requirements.txt

└── README.md

⚙️ How the System Works

Input images are placed in the input/ directory

The main script iterates through all input images

Selected image processing effects are applied automatically

Processed images are saved in the output/ directory

Automated tests verify correct execution and output validity

GitHub Actions CI runs tests on every push to the repository

🧠 Image Processing Techniques:

🎨 Color Pop Effect

Uses grayscale conversion and histogram equalization to enhance contrast, then applies multiple color tints to generate a Warhol-style pop art effect arranged in a 2×2 grid.

⚡ Neon Glow Effect

Applies edge detection, edge thickening, and multi-layer Gaussian blur to simulate neon outlines with glow and bloom effects, similar to modern TikTok neon filters.

🌧️ Rain / Snow Effect

Simulates rain or snow by overlaying randomly generated particle streaks on the image, creating a dynamic weather effect.

😷 Face Mask Detection

Implements a rule-based face mask detection system using Haar Cascade face detection and skin-color analysis on the lower half of detected faces to infer mask presence.

🔄 DevOps & Continuous Integration

GitHub Actions automatically runs tests on every push

Ensures required output folders exist

Validates that image processing functions return valid results

Prevents faulty code from being merged

This ensures the pipeline remains stable and reproducible.

🤖 CI Workflow (GitHub Actions)

The project uses GitHub Actions to implement a Continuous Integration (CI) workflow that automatically validates the codebase.

Workflow Process

A developer pushes code to the GitHub repository

GitHub Actions automatically triggers the CI workflow

The workflow sets up a Python environment

Project dependencies are installed from requirements.txt

Automated tests are executed using pytest

The workflow reports whether the build passed or failed

Purpose of the CI Workflow

Detects errors early in development

Ensures all image processing functions work as expected

Maintains consistent project quality

Enforces DevOps best practices through automation

By integrating GitHub Actions, the project guarantees that every code change is tested and validated before integration.

▶️ How to Run the Project
1. Clone the Repository
git clone <https://github.com/happyvirus-kai/automated-image-processing-devops.git>
cd project-folder
2. Install Dependencies
pip install -r requirements.txt
3. Run the Program
python src/main.py

Processed images will be saved in the output_images/ directory.

🧪 Running Tests

Execute all tests using:

pytest

Tests validate:

Existence of output folders

Successful image processing

Correct output dimensions

⚠️ Limitations

Face mask detection accuracy may vary depending on lighting and face orientation

Image effects are designed for visual demonstration, not real-world deployment

The project focuses on automation and DevOps integration rather than model training

✅ Conclusion

This project demonstrates how image processing systems can be effectively automated using DevOps principles. By integrating Python-based image transformations with automated testing and CI pipelines, the system ensures reliable and repeatable results suitable for educational and demonstration purposes.

👩‍💻 Author

Kyla C. Alicaway

Christian G. Licuanan

Ma. Yvette L. Magana

ELECTIVE 4 Midterm Exam