import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to load and process data
def load_data(file):
    try:
        raw_df = pd.read_excel(file, header=None)
        first_row = raw_df.iloc[0]

        # Determine if first row contains headers
        if all(isinstance(cell, str) for cell in first_row):
            df = pd.read_excel(file, header=0)
        else:
            df = pd.read_excel(file, header=None)
            df.columns = ['x', 'y']
        
        return df[['x', 'y']].dropna()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Function to fit polynomial and plot results
def fit_polynomial(data):
    poly_coeff = np.polyfit(data['x'], data['y'], 3)
    poly_eq = np.poly1d(poly_coeff)

    # Generate fit and derivatives
    x_fit = np.linspace(data['x'].min(), data['x'].max(), 100)
    y_fit = poly_eq(x_fit)
    poly_deriv_1 = poly_eq.deriv(1)
    poly_deriv_2 = poly_eq.deriv(2)
    y_deriv_1 = poly_deriv_1(x_fit)
    y_deriv_2 = poly_deriv_2(x_fit)

    # Find extrema and inflection points
    critical_points = poly_deriv_1.roots
    inflection_points = poly_deriv_2.roots
    extrema = [(p, poly_eq(p)) for p in critical_points]
    inflections = [(p, poly_eq(p)) for p in inflection_points]

    return poly_eq, x_fit, y_fit, y_deriv_1, y_deriv_2, extrema, inflections

# Streamlit App
st.title("Polynomial Fit and Analysis Web App")

uploaded_file = st.file_uploader("Upload Excel File with X and Y Columns", type=["xlsx"])
if uploaded_file:
    data = load_data(uploaded_file)
    if data is not None:
        st.write("### Uploaded Data")
        st.dataframe(data)

        st.write("### Data Plot")
        fig, ax = plt.subplots()
        ax.plot(data['x'], data['y'], 'o', label="Data")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        st.pyplot(fig)

        if st.button("Perform Polynomial Fit"):
            poly_eq, x_fit, y_fit, y_deriv_1, y_deriv_2, extrema, inflections = fit_polynomial(data)

            # Polynomial Fit Plot
            st.write("### Polynomial Fit")
            fig, ax = plt.subplots()
            ax.plot(data['x'], data['y'], 'o', label="Data")
            ax.plot(x_fit, y_fit, label="Polynomial Fit")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            st.pyplot(fig)

            # Show Fit Equation
            st.write(f"**Fit Equation:** {poly_eq}")

            if st.button("Compute Derivatives"):
                # Plot Derivatives
                st.write("### Derivatives")
                fig, ax = plt.subplots()
                ax.plot(x_fit, y_fit, label="Polynomial Fit")
                ax.plot(x_fit, y_deriv_1, label="1st Derivative", color="red")
                ax.plot(x_fit, y_deriv_2, label="2nd Derivative", color="blue")
                ax.legend()
                ax.set_xlabel("x")
                ax.set_ylabel("y")
                st.pyplot(fig)

                # Display Extrema and Inflection Points
                st.write("### Extrema and Inflection Points")
                for p, value in extrema:
                    st.write(f"Extrema: x = {p:.2f}, y = {value:.2f}")
                for p, value in inflections:
                    st.write(f"Inflection Point: x = {p:.2f}, y = {value:.2f}")
