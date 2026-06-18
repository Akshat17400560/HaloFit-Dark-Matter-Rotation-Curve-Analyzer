import streamlit as st

from src.analysis import (
    load_galaxy_data,
    compute_visible_velocity,
    fit_iso_model,
    create_rotation_curve_plot
)

from src.llm_report import generate_report

st.set_page_config(
    page_title="Dark Matter Rotation Curve Analyzer",
    page_icon="📈",
    layout="wide"
)
st.title("📈 Dark Matter Rotation Curve Analyzer")

st.markdown("""
Analyze galaxy rotation curves using an **Isothermal Dark Matter Halo Model**.

Enter a galaxy name from the SPARC dataset and the application will:

- Load observational data
- Fit an Isothermal dark matter halo model
- Estimate halo parameters
- Visualize the rotation curve
- Generate an astrophysical interpretation
""")

st.divider()

with st.sidebar:

    st.header("Galaxy Selection")

    galaxy = st.text_input(
        "Galaxy Name",
        placeholder="Example: NGC1705"
    )

    analyze_btn = st.button(
        "Analyze Galaxy",
        use_container_width=True
    )

if analyze_btn:

    if not galaxy:

        st.warning(
            "Please enter a galaxy name."
        )

    else:

        try:

            with st.spinner(
                f"Analyzing {galaxy}..."
            ):

                file_path = (
                    f"data/{galaxy}_rotmod.dat"
                )

                df = load_galaxy_data(
                    file_path
                )

                df = compute_visible_velocity(
                    df
                )

                result = fit_iso_model(
                    df
                )

                report = generate_report(
                    galaxy,
                    result["rho0"],
                    result["rc"],
                    result["chi2"],
                    result["max_observed_velocity"],
                    result["max_visible_velocity"],
                    result["outer_observed_velocity"],
                    result["outer_visible_velocity"],
                    result["outer_velocity_gap"]
                )

                fig = create_rotation_curve_plot(
                    df,
                    result["pred"],
                    galaxy
                )

            st.success(
                f"Analysis completed for {galaxy} galaxy"
            )

            st.subheader("Halo Fit Parameters")
            c1, c2, c3, c4 = st.columns(4)

            c1.metric("ρ₀", f"{result['rho0']:.2e} M☉/pc³")
            c2.metric("Core Radius (rc)", f"{result['rc']:.2f} kpc")
            c3.metric("χ²", f"{result['chi2']:.2f}")
            c4.metric("Outer Velocity Gap", f"{result['outer_velocity_gap']:.2f} km/s")

            st.subheader("Rotation Curve Characteristics")
            c5, c6, c7, c8 = st.columns(4)

            c5.metric(
                "Max Observed Velocity",
                f"{result['max_observed_velocity']:.2f} km/s"
            )

            c6.metric(
                "Max Visible Velocity",
                f"{result['max_visible_velocity']:.2f} km/s"
            )

            c7.metric(
                "Outer Observed Velocity",
                f"{result['outer_observed_velocity']:.2f} km/s"
            )

            c8.metric(
                "Outer Visible Velocity",
                f"{result['outer_visible_velocity']:.2f} km/s"
            )
            st.divider()

            st.subheader(
                "Rotation Curve"
            )

            st.pyplot(
                fig,
                use_container_width=True
            )

            st.divider()


            st.subheader(
                "Scientific Interpretation"
            )

            with st.expander(
                "View Analysis Report",
                expanded=True
            ):
                st.markdown(report)

        except FileNotFoundError:

            st.error(
                f"Galaxy '{galaxy}' not found."
            )

        except Exception as e:

            st.error(
                f"Analysis failed: {str(e)}"
            )