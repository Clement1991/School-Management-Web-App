INSERT INTO "departments" ("name")
VALUES
("Aeronautics"),
("Bioengineering"),
("Chemical Engineering");


INSERT INTO "programs" ("name", "degree", "department_id", "duration_years")
VALUES
("MEng Aeronautical Engineering", "Undergraduate", 1, 4),
("MEng Aeronautics with Spacecraft Engineering", "Undergraduate", 1, 4),
("MSc Advanced Aeronautical Engineering", "Master", 1, 1),
("MSc Advanced Computational Methods", "Master", 1, 1),
("MEng Biomedical Engineering", "Undergraduate", 2, 4),
("MSc Human and Biological Robotics", "Master", 2, 1),
("MEng Chemical Engineering", "Undergraduate", 3, 4);


INSERT INTO "courses" ("name")
VALUES
("Aerodynamics 1"),
("Computing and Numerical Methods 1"),
("Engineering Practice 1"),
("Introduction to Aerospace"),
("Materials 1"),
("Mathematics 1"),
("Mechanics"),
("Structures 1"),
("Thermodynamics and Heat Transfer"),
("Aerodynamics 2"),
("Computing and Numerical Methods 2"),
("Engineering Practice 2 – Project Development"),
("Engineering Practice 2 – Technical"),
("Flight Dynamics and Control"),
("Materials 2"),
("Mathematics 2"),
("Mechatronics"),
("Propulsion and Turbomachinery"),
("Structures 2"),
("Aerodynamics 3"),
("Aerospace Vehicle Design"),
("Control Systems"),
("Group Design Project"),
("Structures 3"),
("Finite Elements"),
("Orbital Mechanics"),
("Advanced Fluid Dynamics and Fluid-Structure Interaction"),
("Mathematics 3"),
("Turbulence and Turbulence Modelling"),
("Individual Project"),
("Computational Fluid Dynamics"),
("Computational Mechanics"),
("Advanced Propulsion"),
("Innovation Management"),
("Advanced Manufacturing"),
("High Performance Computing"),
("Spacecraft Systems"),
("Spacecraft Structures"),
("Applications of Fluid Dynamics"),
("Applications of Computational Fluid Dynamics"),
("Lightweight Structures"),
("Aeroelasticity"),
("Optimisation (IDX)"),
("Design for Additive Manufacturing (IDX)"),
("Flow Instability and Transition"),
("Artificial Intelligence for Aerospace Engineers"),
("BPES / Horizons (level 6 or 7)"),
("Aerospace Structures"),
("Aircraft Design and Airworthiness"),
("Applied Aerodynamics"),
("Emerging Technology for Green Aviation"),
("Major Individual Research Project"),
("Control Theory for Flow Management"),
("Systems Engineering for Unmanned Aerial Vehicles"),
("Molecules and Energetics 1"),
("Medical and Biochemical Science 1"),
("Mathematics and Engineering 1"),
("Computer Fundamentals and Programming 1"),
("Design and Professional Practice 1"),
("Molecules, Materials and Measurement 2"),
("Medical and Biochemical Science 2"),
("Mathematics and Engineering 2"),
("Design and Professional Practice 2"),
("Programming 2"),
("Probability and Statistics for Bioengineering"),
("Bioengineering Group Project"),
("Biomaterials for Bioengineers"),
("Foundations of Synthetic Biology"),
("Modelling in Biology"),
("Individual Project*"),
("Advanced Synthetic Biology*"),
("Advanced Chemical Sensors*"),
("Advanced Physiological Monitoring and Data Analysis*"),
("Molecular and Tissue Imaging*"),
("Medical Device Entrepreneurship*"),
("Reinforcement Learning"),
("Robotics 1: Introduction to Robotics"),
("Systems Physiology"),
("Statistics and Data Analysis"),
("Human Neuromechanical Control and Learning"),
("Medical Device Entrepreneurship"),
("Biomechanics"),
("Biomimetics"),
("Brain Machine Interfaces"),
("Computational Neuroscience"),
("Computer Vision and Pattern Recognition"),
("Image Processing"),
("Major Individual Project"),
("Mastery 1"),
("Process Analysis"),
("Chemical Engineering Practice 1"),
("Transfer Processes 1"),
("Thermodynamics 1"),
("Separation Processes 1"),
("Chemistry 1"),
("Mathematics Fundamentals"),
("Physical Chemistry"),
("Mastery 2"),
("Transfer Processes 2"),
("Chemical Engineering Practice 2"),
("Reaction Engineering 1"),
("Thermodynamics 2"),
("Process Dynamics and Control"),
("Separation Processes 2"),
("Engineering Mathematics"),
("Chemistry 2"),
("Mastery 3"),
("Reaction Engineering 2"),
("Particle Engineering"),
("Process Design"),
("Safety and Loss Prevention"),
("Environmental Engineering"),
("Chemical Engineering Practice 3"),
("Process Optimisation"),
("Nuclear Chemical Engineering"),
("Carbon Capture and Clean Fossil Fuels"),
("Chemical Engineering Practice 4"),
("Colloids and Interface Science"),
("Product Characterisation"),
("Applied Spectroscopy"),
("Biochemical Engineering"),
("Advanced Process Operations"),
("Advanced Process Optimisation"),
("Dynamic Behaviour of Process Systems");


INSERT INTO "outlines" ("program_id", "course_id", "year")
VALUES
(1, 1, 1),
(1, 2, 1),
(1, 3, 1),
(1, 4, 1),
(1, 5, 1),
(1, 6, 1),
(1, 7, 1),
(1, 8, 1),
(1, 9, 1),
(1, 10, 2),
(1, 11, 2),
(1, 12, 2),
(1, 13, 2),
(1, 14, 2),
(1, 15, 2),
(1, 16, 2),
(1, 17, 2),
(1, 18, 2),
(1, 19, 2),
(1, 20, 3),
(1, 21, 3),
(1, 22, 3),
(1, 23, 3),
(1, 24, 3),
(1, 25, 3),
(1, 26, 3),
(1, 27, 3),
(1, 28, 3),
(1, 29, 3),
(1, 30, 4),
(1, 31, 4),
(1, 32, 4),
(1, 33, 4),
(1, 34, 4),
(1, 35, 4),
(1, 36, 4),
(1, 37, 4),
(1, 38, 4),
(1, 39, 4),
(1, 40, 4),
(2, 1, 1),
(2, 2, 1),
(2, 3, 1),
(2, 4, 1),
(2, 5, 1),
(2, 6, 1),
(2, 7, 1),
(2, 8, 1),
(2, 9, 1),
(2, 10, 2),
(2, 11, 2),
(2, 12, 2),
(2, 13, 2),
(2, 14, 2),
(2, 15, 2),
(2, 16, 2),
(2, 17, 2),
(2, 18, 2),
(2, 19, 2),
(2, 20, 3),
(2, 21, 3),
(2, 22, 3),
(2, 23, 3),
(2, 24, 3),
(2, 26, 3),
(2, 37, 3),
(2, 38, 3),
(2, 40, 4),
(2, 41, 4),
(2, 42, 4),
(2, 43, 4),
(2, 44, 4),
(2, 45, 4),
(2, 46, 4),
(2, 47, 4),
(3, 48, 1),
(3, 49, 1),
(3, 50, 1),
(3, 51, 1),
(3, 52, 1),
(3, 31, 1),
(3, 32, 1),
(3, 33, 1),
(3, 34, 1),
(3, 35, 1),
(4, 27, 1),
(4, 49, 1),
(4, 50, 1),
(4, 51, 1),
(4, 52, 1),
(4, 25, 1),
(4, 34, 1),
(4, 45, 1),
(4, 53, 1),
(4, 54, 1),
(5, 55, 1),
(5, 56, 1),
(5, 57, 1),
(5, 58, 1),
(5, 59, 1),
(5, 60, 2),
(5, 61, 2),
(5, 62, 2),
(5, 63, 2),
(5, 64, 2),
(5, 65, 3),
(5, 66, 3),
(5, 67, 3),
(5, 68, 3),
(5, 69, 3),
(5, 70, 4),
(5, 71, 4),
(5, 72, 4),
(5, 73, 4),
(5, 74, 4),
(5, 75, 4),
(6, 76, 1),
(6, 77, 1),
(6, 78, 1),
(6, 79, 1),
(6, 80, 1),
(6, 81, 1),
(6, 82, 1),
(6, 83, 1),
(6, 84, 1),
(6, 85, 1),
(6, 86, 1),
(6, 87, 1),
(6, 88, 1),
(6, 89, 1),
(6, 90, 1),
(6, 91, 1),
(6, 92, 1),
(6, 93, 1),
(6, 94, 1),
(6, 95, 1),
(6, 96, 1),
(6, 97, 1),
(7, 89, 1),
(7, 90, 1),
(7, 91, 1),
(7, 92, 1),
(7, 93, 1),
(7, 94, 1),
(7, 95, 1),
(7, 96, 1),
(7, 97, 1),
(7, 98, 2),
(7, 99, 2),
(7, 100, 2),
(7, 101, 2),
(7, 102, 2),
(7, 103, 2),
(7, 104, 2),
(7, 105, 2),
(7, 106, 2),
(7, 107, 3),
(7, 108, 3),
(7, 109, 3),
(7, 110, 3),
(7, 111, 3),
(7, 112, 3),
(7, 113, 3),
(7, 114, 3),
(7, 115, 3),
(7, 116, 3),
(7, 117, 4),
(7, 118, 4),
(7, 119, 4),
(7, 120, 4),
(7, 121, 4),
(7, 122, 4),
(7, 123, 4),
(7, 124, 4);
