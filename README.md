"# CS263_Project" 

Make sure you have python and rust installed

To install rust, go to rustup and download rustup-init.exe. Then follow the instructions that pop up. Then download build tools for visual studio from aka.ms/vs/stable/vs_BuildTools.exe. Then when installing it, check Desktop development with C++.

For graphs, you have to install pandas and matplotlib "pip install pandas" "pip install matplotlib"
For Dijkstras Correctness tests in python, you have to install networkx "pip install networkx"

Graphs are located in {Alogrithm}/{Language}/{Round #}/{Performance_Test#}

For Python Quicksort Correctness tests, first, go to the Python folder inside of the quicksort folder. Take all of the generated implementations from any of the rounds and move them into Quicksort/Python folder. Then run the command "python QuickSort_Correctness.py" in the Quicksort/Python folder.

For Rust Quicksort Correctness tests, first go to the Rust folder inside of the quicksort folder. Copy all of the generated implementations from any of the rounds and paste them into the src folder as well as the bin folder. (They need to be present in both folders) Then, run the command "cargo run --bin quicksort_correctness" in the Quicksort/Rust folder.

For Python Quicksort Performance tests, first, go to the Python folder inside of the QuickSort folder. Take all of the generated implementations from any of the rounds and move them into Quicksort/Python folder. (If you already did this for the correctness step then you do not have to do this first part) Then run the command "python QuickSort_Performance.py" in the Quicksort/Python folder. To get the graphs for these performance tests, simply run "python pythonqs_make_plots.py" in the same folder. 

For Rust Quicksort Performance tests, first go to the Rust folder inside of the quicksort folder. Copy all of the generated implementations from any of the rounds and paste them into the src folder as well as the bin folder. (They need to be present in both folders) (If you have already done this for the correctness step then you do not have to do this first part) Then, run the command "cargo run --bin quicksort_performance --release" in the Quicksort/Rust folder. To get the graphs for these performance tests, simply run "python rustqs_make_plots.py" in the same folder. 

For Python Dijkstra Correctness tests, first, go to the Python folder inside of the Dijkstras folder. Take all of the generated implementations from any of the rounds and move them into Dijkstras/Python folder. Then run the command "python Dijkstras_Correctness.py" in the Dijkstras/Python folder.

For Rust Dijkstra Correctness tests, first, go to the Rust folder inside of the Dijkstras folder. Copy all of the generated implementations from any of the rounds and paste them into the src folder as well as the bin folder. (They need to be present in both folders) Then, run the command "cargo run --bin dijkstras_correctness" in the Dijkstras/Rust folder.

For Python Dijkstra Performance tests, first, go to the Python folder inside of the Dijkstras folder. Take all of the generated implementations from any of the rounds and move them into Dijkstras/Python folder. (If you already did this for the correctness step then you do not have to do this first part) Then run the command "python Dijkstras_Performance.py" in the Dijkstras/Python folder. To get the graphs for these performance tests, simply run "python pythondj_make_plots.py" in the same folder.

For Rust Dijkstra Performance tests, first go to the Rust folder inside of the Dijkstras folder. Copy all of the generated implementations from any of the rounds and paste them into the src folder as well as the bin folder. (They need to be present in both folders) (If you have already done this for the correctness step then you do not have to do this first part) Then, run the command "cargo run --bin dijkstras_performance --release" in the Dijkstras/Rust folder. To get the graphs for these performance tests, simply run "python rustdj_make_plots.py" in the same folder.


