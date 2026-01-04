"""
Lütkepohl Consumption-Investment Cointegration Analysis
=======================================================

This script demonstrates the complete workflow for analyzing cointegration
with structural breaks using the Lütkepohl dataset.

Dataset: West German quarterly macroeconomic data (1960Q1-1982Q4)
Variables: CONS (log consumption), INV (log investment)
Model: CONS = μ + β*INV + u (with potential structural breaks)
Configuration: max_breaks=2, dynamic_lags=2

Based on Schmidt and Schweikert (2021):
"Multiple structural breaks in cointegrating regressions: A model selection approach"
Studies in Nonlinear Dynamics & Econometrics.

Author: Dr. Merwan Roudane
"""

import numpy as np
import pandas as pd
import warnings
from selectbreakcoint import (
    AdaptiveLassoBreaks, 
    CointegrationTest,
    adf_test,
    engle_granger_test,
    gregory_hansen_test,
    hatemi_j_test
)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=RuntimeWarning)


def main():
    """Run the Lütkepohl consumption-investment analysis."""
    
    print("=" * 70)
    print("Lütkepohl Consumption-Investment Cointegration Analysis")
    print("Based on Schmidt and Schweikert (2021)")
    print("=" * 70)
    print()
    
    # =========================================================================
    # Load Data
    # =========================================================================
    data_path = "data/lutkepohl2.xlsx"
    
    try:
        data = pd.read_excel(data_path)
        print(f"Data loaded: {len(data)} quarterly observations")
        print(f"Period: {data.iloc[0, 0]} to {data.iloc[-1, 0]}")
        print(f"Variables: {list(data.columns)}")
        print()
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        print("Please ensure lutkepohl2.xlsx is in the data directory.")
        return
    
    # Extract variables
    cons = data['CONS'].values  # Log consumption (dependent)
    inv = data['INV'].values    # Log investment (independent)
    T = len(cons)
    
    print(f"CONS (dependent): mean={cons.mean():.4f}, std={cons.std():.4f}")
    print(f"INV (independent): mean={inv.mean():.4f}, std={inv.std():.4f}")
    print()
    
    # =========================================================================
    # Step 1: Unit Root Tests
    # =========================================================================
    print("-" * 70)
    print("Step 1: Unit Root Tests (ADF)")
    print("-" * 70)
    
    # Levels
    adf_cons, lag_cons, _ = adf_test(cons)
    adf_inv, lag_inv, _ = adf_test(inv)
    print(f"\nLevels:")
    print(f"  CONS: ADF = {adf_cons:.4f} (lag={lag_cons})")
    print(f"  INV:  ADF = {adf_inv:.4f} (lag={lag_inv})")
    
    # First differences
    adf_d_cons, lag_d_cons, _ = adf_test(np.diff(cons))
    adf_d_inv, lag_d_inv, _ = adf_test(np.diff(inv))
    print(f"\nFirst Differences:")
    print(f"  ΔCONS: ADF = {adf_d_cons:.4f} (lag={lag_d_cons})")
    print(f"  ΔINV:  ADF = {adf_d_inv:.4f} (lag={lag_d_inv})")
    print(f"\n5% critical value ≈ -2.89")
    print("Conclusion: Both series appear to be I(1)")
    print()
    
    # =========================================================================
    # Step 2: Engle-Granger Test (No Structural Breaks)
    # =========================================================================
    print("-" * 70)
    print("Step 2: Engle-Granger Test (assuming no structural breaks)")
    print("-" * 70)
    
    eg_result = engle_granger_test(cons, inv)
    print(f"\nModel: CONS = μ + β*INV + u")
    print(f"  Test statistic: {eg_result.test_statistic:.4f}")
    print(f"  Critical values: 10%: {eg_result.critical_values.get(0.10, 'N/A'):.2f}, "
          f"5%: {eg_result.critical_values.get(0.05, 'N/A'):.2f}, "
          f"1%: {eg_result.critical_values.get(0.01, 'N/A'):.2f}")
    print(f"  Reject H0 (no cointegration) at 5%: {eg_result.is_cointegrated}")
    print()
    
    # =========================================================================
    # Step 3: Gregory-Hansen Test (One Structural Break)
    # =========================================================================
    print("-" * 70)
    print("Step 3: Gregory-Hansen Test (allowing for one structural break)")
    print("-" * 70)
    
    gh_result = gregory_hansen_test(cons, inv, model='C/S', trim=0.15)
    print(f"\nModel: Regime Shift (C/S)")
    print(f"  Test statistic: {gh_result.test_statistic:.4f}")
    print(f"  Critical values: 10%: {gh_result.critical_values.get(0.10, 'N/A'):.2f}, "
          f"5%: {gh_result.critical_values.get(0.05, 'N/A'):.2f}, "
          f"1%: {gh_result.critical_values.get(0.01, 'N/A'):.2f}")
    print(f"  Reject H0 at 5%: {gh_result.is_cointegrated}")
    if len(gh_result.break_dates) > 0:
        break_idx = int(gh_result.break_dates[0])
        if break_idx < len(data):
            print(f"  Estimated break: {data.iloc[break_idx, 0]} (t={break_idx})")
    print()
    
    # =========================================================================
    # Step 4: Hatemi-J Test (Two Structural Breaks)
    # =========================================================================
    print("-" * 70)
    print("Step 4: Hatemi-J Test (allowing for two structural breaks)")
    print("-" * 70)
    
    hj_result = hatemi_j_test(cons, inv, trim=0.15)
    print(f"\n  Test statistic: {hj_result.test_statistic:.4f}")
    print(f"  Critical values: 10%: {hj_result.critical_values.get(0.10, 'N/A'):.2f}, "
          f"5%: {hj_result.critical_values.get(0.05, 'N/A'):.2f}, "
          f"1%: {hj_result.critical_values.get(0.01, 'N/A'):.2f}")
    print(f"  Reject H0 at 5%: {hj_result.is_cointegrated}")
    if len(hj_result.break_dates) > 0:
        for i, break_idx in enumerate(hj_result.break_dates):
            idx = int(break_idx)
            if idx < len(data):
                print(f"  Break {i+1}: {data.iloc[idx, 0]} (t={idx})")
    print()
    
    # =========================================================================
    # Step 5: Adaptive Lasso Approach (Up to 2 Structural Breaks)
    # =========================================================================
    print("-" * 70)
    print("Step 5: Adaptive Lasso Approach (max_breaks=2, dynamic_lags=2)")
    print("-" * 70)
    print("  Method: Algorithm 1 from Schmidt and Schweikert (2021)")
    print()
    
    # Run the adaptive lasso break detection
    model = AdaptiveLassoBreaks(
        max_breaks=2, 
        trim=0.05,
        dynamic_lags=2  # Endogeneity correction with 2 leads/lags
    )
    
    break_result = model.fit(inv, cons)
    
    print(f"  Number of breaks detected: {break_result.n_breaks}")
    print()
    
    if break_result.n_breaks > 0:
        print("  Estimated break dates:")
        for i, (frac, date_idx) in enumerate(zip(break_result.break_fractions, 
                                                  break_result.break_dates)):
            idx = int(date_idx)
            if idx < len(data):
                date_str = data.iloc[idx, 0]
            else:
                date_str = f"t={idx}"
            print(f"    Break {i+1}: {date_str} (τ = {frac:.4f})")
        print()
        
        print("  Regime coefficients:")
        for i, (mu, beta) in enumerate(zip(break_result.regime_intercepts, 
                                           break_result.regime_slopes)):
            print(f"    Regime {i+1}: CONS = {mu:.4f} + {beta:.4f} × INV")
        print()
        
        print("  Parameter changes at breaks:")
        for i, (d_mu, d_beta) in enumerate(zip(break_result.intercept_changes,
                                                break_result.slope_changes)):
            print(f"    Break {i+1}: Δμ = {d_mu:.4f}, Δβ = {d_beta:.4f}")
    else:
        print(f"  No breaks detected.")
        print(f"  Estimated model: CONS = {break_result.regime_intercepts[0]:.4f} + "
              f"{break_result.regime_slopes[0]:.4f} × INV")
    print()
    
    print(f"  Model fit:")
    print(f"    BIC: {break_result.bic:.4f}")
    print(f"    MSE: {break_result.mse:.6f}")
    print(f"    SSR: {break_result.ssr:.4f}")
    print()
    
    # Run cointegration test with structural breaks
    test = CointegrationTest(
        max_breaks=2, 
        test_type='adf',
        lag_selection='aic',
        dynamic_lags=2
    )
    
    test_result = test.test(inv, cons)
    
    print(f"  Cointegration Test (ADF-type):")
    print(f"    Test statistic: {test_result.test_statistic:.4f}")
    print(f"    Critical values: 10%: {test_result.critical_values.get(0.10, 'N/A'):.2f}, "
          f"5%: {test_result.critical_values.get(0.05, 'N/A'):.2f}, "
          f"1%: {test_result.critical_values.get(0.01, 'N/A'):.2f}")
    print(f"    Reject H0 at 5%: {test_result.is_cointegrated}")
    print()
    
    # =========================================================================
    # Step 6: Summary
    # =========================================================================
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("Cointegration relationship: CONS = μ + β × INV")
    print(f"Sample: {T} quarterly observations (1960Q1-1982Q4)")
    print()
    print("Test Results:")
    print(f"  {'Method':<30} {'Statistic':>10} {'Cointegrated':>15}")
    print(f"  {'-'*55}")
    print(f"  {'Engle-Granger (0 breaks)':<30} {eg_result.test_statistic:>10.4f} {str(eg_result.is_cointegrated):>15}")
    print(f"  {'Gregory-Hansen (1 break)':<30} {gh_result.test_statistic:>10.4f} {str(gh_result.is_cointegrated):>15}")
    print(f"  {'Hatemi-J (2 breaks)':<30} {hj_result.test_statistic:>10.4f} {str(hj_result.is_cointegrated):>15}")
    print(f"  {'Adaptive Lasso (≤2 breaks)':<30} {test_result.test_statistic:>10.4f} {str(test_result.is_cointegrated):>15}")
    print()
    
    print("Key Findings:")
    print(f"  - Structural breaks detected: {break_result.n_breaks}")
    if break_result.n_breaks > 0:
        print("  - The consumption-investment relationship shows evidence of")
        print("    structural change during the sample period")
        print("  - Accounting for breaks may yield stronger evidence of cointegration")
        print("  - The long-run equilibrium parameters differ across regimes")
    else:
        print("  - No structural breaks detected in the relationship")
        print("  - Standard cointegration methods may be appropriate")
    print()


if __name__ == "__main__":
    main()
