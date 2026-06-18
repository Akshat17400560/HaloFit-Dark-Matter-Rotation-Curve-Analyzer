from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
load_dotenv()
def generate_report(
    galaxy,
    rho0,
    rc,
    chi2,
    max_observed_velocity,
    max_visible_velocity,
    outer_observed_velocity,
    outer_visible_velocity,
    outer_velocity_gap
):

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_template(
    """
    You are a research astrophysicist analyzing a galaxy rotation curve.

    Your task is to analyze ONLY the supplied measurements and fitted results. Base every conclusion on the provided data. Avoid generic explanations of dark matter, galaxy formation, or astrophysics unless they are directly supported by the measurements.

    Galaxy: {galaxy}

    Isothermal Halo Fit Parameters:

    Central Density (rho0): {rho0}
    Core Radius (rc): {rc} kpc

    Fit Statistics:
    Reduced Chi Square: {chi2}
    

    Rotation Curve Properties:

    Maximum Observed Velocity: {max_observed_velocity} km/s
    Maximum Visible Matter Velocity: {max_visible_velocity} km/s
    Outer Observed Velocity: {outer_observed_velocity} km/s
    Outer Visible Matter Velocity: {outer_visible_velocity} km/s
    Outer Velocity Gap: {outer_velocity_gap} km/s

    Write a scientific report with the following sections:

    Rotation Curve Summary

    Describe the overall behavior of the observed rotation curve using the supplied velocity measurements. Compare the observed velocities with the visible matter contribution.

    Dark Matter Halo Analysis

    Interpret the fitted values of rho0 and rc. Discuss what they suggest about the structure and spatial extent of the dark matter halo in this galaxy.

    Fit Quality Assessment

    Evaluate the fit quality using the chi-square value, mean residual, and maximum residual. Discuss whether the isothermal halo model appears to reproduce the observed data successfully.

    Evidence for Dark Matter

    Use the difference between the observed and visible matter velocities, especially at large radii, to discuss the necessity and significance of an additional mass component.

    Conclusion

    Provide a concise scientific conclusion focused specifically on this galaxy and this fit.

    Requirements:

    Use the numerical values in your reasoning.
    Refer to actual measurements whenever possible.
    Do not provide textbook explanations.
    Do not discuss topics not supported by the supplied data.
    Write in the style of a short scientific analysis report.
    """
    )

    chain = prompt | llm

    result = chain.invoke(
        {
            "galaxy": galaxy,
            "rho0": rho0,
            "rc": rc,
            "chi2": chi2,
            "max_observed_velocity":max_observed_velocity,
            "max_visible_velocity":max_visible_velocity,
            "outer_observed_velocity":outer_observed_velocity,
            "outer_visible_velocity":outer_visible_velocity,
            "outer_velocity_gap":outer_velocity_gap
        }
    )

    return result.content