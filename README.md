# 🧠 3D Rubik’s Cube Solver (Python + Pygame)

## 🔷 Overview

This project is a fully functional **3D Rubik's Cube Simulator and Solver** built using **Python**, **NumPy**, and **Pygame**. It simulates the real-world logic of solving a 3×3 cube and provides a visual, interactive interface for scrambling, solving, and manual operations.

The project was developed as part of the **Design Dexterity Challenge** in AeroHack’25 by Collins Aerospace.

---

## 🚀 Features

- ✅ **3D Cube Rendering with Rotation & Lighting**
- ✅ **Manual Move Controls (U, D, L, R, F, B and their inverses)**
- ✅ **Automatic Scramble (25 random moves)**
- ✅ **One-click Solve using inverse move logic**
- ✅ **Step-by-step move animations**
- ✅ **Real-time cube interaction via mouse drag**
- ✅ **Selectable solve speed (Slow, Normal, Fast)**

---

## 🧩 How the Cube is Represented

- The cube is stored as a **NumPy 3D array** of shape `(6, 3, 3)`, where:
  - `6` = Number of faces (`U`, `D`, `L`, `R`, `F`, `B`)
  - `3×3` = Grid of stickers on each face
- Moves are applied by **rotating faces** and updating **adjacent rows/columns** using slicing and `np.rot90`.

## 🕹️ Controls

- `U`, `D`, `L`, `R`, `F`, `B`: Apply face moves  
- `U'`, `D'`, etc.: Apply inverse moves  
- 🎮 **Scramble**: Randomizes cube with 25 valid
moves  
- ⚡ **Solve**: Reverses scramble steps to return to solved state  
- 🌀 **Rotate Cube View**: Drag with mouse  
- 🔘 **Speed Buttons**: Toggle animation speed

---

## 💡 How Solving Works

- The **scramble history** is stored during random shuffling.
- Solving is done by **reversing** that history (`move → move'`).
- This simple inverse logic guarantees a solved cube in minimal steps.

**Example:**  
Scramble: `U F' R D`  
Solution: `D' R' F U'`

---

## 🖼️ Screenshots (Optional for PPT)

- Initial Solved Cube  
- After Scramble  
- Step-by-step Solve (with animation)  
- Final Solved View



---

## 🧠 Concepts Applied

- 3D Matrix Manipulation (NumPy)
- Graphical Rendering (Pygame)
- State Prediction & Move Tracking
- Vector-based Lighting & Shading
- Animation Timing and Queuing
- Event-Driven Programming (Button Inputs)

---

## 📦 Deliverables (For Submission)

- ✅ PowerPoint file (Rubik’s Cube Presentation)
- ✅ All project files (`.py`, assets)
- ✅ README.md (this file)
- ✅  Screenshots

---

## 📜 License

This project is submitted as part of AeroHack’25 and is intended for academic evaluation and recruitment by Collins Aerospace.

## 👨‍💻 Developer

**Name:** Shaik Haseeb  
**Event:** AeroHack’25 – Collins Aerospace  
**Round:** Design Dexterity Challenge  