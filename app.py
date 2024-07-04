import streamlit as st
from scheduling_solver.data_reader import ler_instancia
from scheduling_solver.solver import solve_scheduling_problem

st.title("Single Machine Scheduling Problem Solver")

uploaded_file = st.file_uploader("Choose a file", type="txt")

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    result = solve_scheduling_problem(uploaded_file)

    if 'infeasible' in result:
        st.write("The model is infeasible. Please check the input data.")
    else:
        st.write(f"Optimal makespan (C_max): {result['C_max']}")
        st.write("Order of tasks:")
        for i, j in result['order']:
            st.write(f"Task {i} is followed by Task {j}")

        st.write("Start and completion times of tasks:")
        for j, start, end in result['times']:
            st.write(f"Task {j}: Start = {start}, End = {end}")