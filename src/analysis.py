import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit


G = 4.3009e-6

def load_galaxy_data(file_path):

    df = pd.read_csv(
        file_path,
        sep=r"\s+",
        comment="#",
        header=None
    )

    df.columns = [
        "Rad", "Vobs", "errV",
        "Vgas", "Vdisk", "Vbul",
        "SBdisk", "SBbul"
    ]

    return df

def compute_visible_velocity(df):

    df["Vtheo"] = np.sqrt(
        df["Vgas"]**2 +
        df["Vdisk"]**2 +
        df["Vbul"]**2
    )

    return df

def iso_velocity(r, rho0, rc):

    term = 1 - (rc/r) * np.arctan(r/rc)

    return np.sqrt(
        4*np.pi*G*rho0*(rc**2)*term
    )

def fit_iso_model(df):

    def total_model(r, rho0, rc):

        vhalo = iso_velocity(
            r,
            rho0,
            rc
        )

        return np.sqrt(
            df["Vgas"]**2 +
            df["Vdisk"]**2 +
            df["Vbul"]**2 +
            vhalo**2
        )

    params, cov = curve_fit(
        total_model,
        df["Rad"],
        df["Vobs"],
        p0=[5e7, 2]
    )

    rho0_fit, rc_fit = params

    pred = total_model(
        df["Rad"],
        rho0_fit,
        rc_fit
    )
    max_observed_velocity=df["Vobs"].max()
    max_visible_velocity=df["Vtheo"].max()
    outer_observed_velocity = df["Vobs"].iloc[-1]
    outer_visible_velocity = df["Vtheo"].iloc[-1]
    velocity_gap = (
    outer_observed_velocity
    - outer_visible_velocity
    )
    chi2 = np.sum(
        (
            (df["Vobs"] - pred)
            / df["errV"]
        )**2
    )
    chi2=chi2/(len(df)-2)
    return {
        "rho0": rho0_fit,
        "rc": rc_fit,
        "chi2": chi2,
        "max_observed_velocity":max_observed_velocity,
        "max_visible_velocity": max_visible_velocity,
        "outer_observed_velocity": outer_observed_velocity,
        "outer_visible_velocity": outer_visible_velocity,
        "outer_velocity_gap":velocity_gap,
        "pred": pred
    }


def create_rotation_curve_plot(
    df,
    pred,
    galaxy_name
):

    fig, ax = plt.subplots(
        figsize=(10, 6)
    )

    ax.plot(
        df["Rad"],
        df["Vobs"],
        'ko-',
        label="Observed"
    )

    ax.plot(
        df["Rad"],
        df["Vtheo"],
        label="Baryonic Matter"
    )

    ax.plot(
        df["Rad"],
        pred,
        'r-',
        linewidth=3,
        label="ISO Fit"
    )

    ax.plot(
        df["Rad"],
        df["Vgas"],
        label="VGas"
    )

    ax.plot(
        df["Rad"],
        df["Vdisk"],
        label="VDisk"
    )

    if (df["Vbul"] > 0).any():

        ax.plot(
            df["Rad"],
            df["Vbul"],
            label="VBulge"
        )

    ax.set_title(
        f"{galaxy_name} Rotation Curve"
    )

    ax.set_xlabel(
        "Radius (kpc)"
    )

    ax.set_ylabel(
        "Velocity (km/s)"
    )

    ax.grid(True)
    ax.legend()

    return fig