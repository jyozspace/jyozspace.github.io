# Read the course

These are the authoritative, standalone Markdown notes. Keep assets/ beside lessons/, annexes/ and assessment/ so illustrations work in a local viewer. The website reads these same documents. The downloadable course-notes.zip includes linked app/source artifacts for offline reading.

## Start here

1. [00 · Your robotics workbench](lessons/00-setup-guide.md)
2. [01 · From a robot to the ROS graph](lessons/01-lecture1-architecture.md)
3. [02 · Write your first Python nodes](lessons/02-lecture2-python-nodes.md)
4. [03 · The same graph, in C++](lessons/03-lecture3-cpp-nodes.md)
5. [04 · Connect a complete system](lessons/04-lecture4-services-actions-tf.md)
6. [05 · A phone that helps build a map](lessons/05-lecture5-sensors-slam.md)

## Practical annexes

- [A: Android app development](annexes/android-development.md)
- [B: ROS receiver development](annexes/bridge-development.md)
- [C: Camera and IMU calibration](annexes/calibration.md)
- [D: More ROS workflows](annexes/ros-workflows.md)
- [E: Connect Android by USB or wireless](annexes/android-connections.md)
- [F: WSL 2 capstone](annexes/wsl-capstone.md)
- [G: Sharing Windows and Linux files](annexes/wsl-files.md)
- [H: Forwarding USB sensors into WSL](annexes/wsl-usb.md)
- [I: Windows–Linux networking](annexes/wsl-networking.md)

## References and assessment

- [Phone lab preparation](annexes/dataset-guide.md)
- [Frames and transforms](annexes/frames.md)
- [Command field guide](annexes/cheatsheet-cli.md)
- [Sensor clients and receiver contracts](annexes/phone-app.md)
- [Visual checkpoints](annexes/visual-guide.md)
- [Visual sources and licenses](annexes/visual-sources.md)
- [Troubleshooting](annexes/troubleshooting.md)
- [Official references and glossary](annexes/references.md)
- [Course scope and learning outcomes](annexes/verification.md)
- [Scenario quiz bank](assessment/quiz-bank.md)
- [Written prompts and model explanations](assessment/descriptive-questions.md)
- [Worked exercise explanations and rubric](assessment/exercise-solutions.md)

Quizzes and written prompts are generated from maintenance/tools/course-meta.mjs. Edit that metadata to change the questions; edit the other Markdown files directly. Concept diagrams explain relationships; simulated interfaces and upstream screenshots are labelled individually. Use your own captured evidence in student reports. Expected-output blocks are labelled and use a distinct blue panel without a Copy button on the website.

Course text and original teaching diagrams are licensed under CC BY 4.0. Third-party images retain their credited licenses; see the visual source register. Preserve attribution when sharing. Code archives include their own licenses: Apache-2.0 for the core and Android app, GPL-3.0-or-later for the optional SLAM adapter.
