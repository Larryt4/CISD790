import unittest
import matplotlib.pyplot as plt
import numpy as np
from unittest.mock import patch, MagicMock
import warnings


class TestMatplotlibIntegration(unittest.TestCase):
    """Integration tests for matplotlib plotting workflows similar to the notebook context."""
    
    def setUp(self):
        """Set up test data similar to baseball data from the notebook context."""
        # Mock baseball data structure
        self.bball_data = {
            'Payroll': np.array([50, 75, 100, 125, 150, 175, 200]),
            'WinPct': np.array([0.35, 0.42, 0.48, 0.55, 0.62, 0.68, 0.75])
        }
        
    def tearDown(self):
        """Clean up matplotlib state after each test."""
        plt.close('all')
        plt.clf()
    
    @patch('matplotlib.pyplot.show')
    def test_polyfit_visualization_workflow(self, mock_show):
        """Test the complete polyfit and visualization workflow from the notebook."""
        # Recreate the exact workflow from the notebook context
        payroll = self.bball_data['Payroll']
        winpct = self.bball_data['WinPct']
        
        # Perform polynomial fit (degree 1 = linear)
        p = np.polyfit(payroll, winpct, 1)
        
        # Create the plot with fitted line
        plt.plot(payroll, np.polyval(p, payroll), 'g-')
        
        # Show the plot (this should work correctly)
        plt.show()
        
        # Verify the show method was called
        mock_show.assert_called_once()
        
        # Verify polynomial coefficients are reasonable
        self.assertEqual(len(p), 2, "Linear fit should return 2 coefficients")
        self.assertGreater(p[0], 0, "Slope should be positive for payroll vs win percentage")
    
    def test_matplotlib_show_method_signature(self):
        """Test that plt.show() has the expected method signature."""
        import inspect
        
        # Get the signature of plt.show
        show_signature = inspect.signature(plt.show)
        
        # plt.show() should be callable without required arguments
        try:
            # This should not raise an exception
            show_signature.bind()
            signature_valid = True
        except TypeError:
            signature_valid = False
        
        self.assertTrue(signature_valid, "plt.show() should be callable without arguments")
    
    def test_invalid_matplotlib_methods_raise_errors(self):
        """Test that calling non-existent matplotlib methods raises appropriate errors."""
        invalid_methods = ['show2', 'show3', 'display2', 'render3']
        
        for method_name in invalid_methods:
            with self.subTest(method=method_name):
                with self.assertRaises(AttributeError, 
                                     msg=f"plt.{method_name} should raise AttributeError"):
                    getattr(plt, method_name)()
    
    @patch('matplotlib.pyplot.show')
    def test_multiple_show_calls_behavior(self, mock_show):
        """Test behavior when plt.show() is called multiple times (which is valid)."""
        # Create multiple plots
        plt.figure(1)
        plt.plot([1, 2, 3], [1, 4, 9])
        plt.show()
        
        plt.figure(2)
        plt.plot([1, 2, 3], [1, 2, 3])
        plt.show()
        
        # Multiple show calls should work fine
        self.assertEqual(mock_show.call_count, 2, 
                        "Multiple plt.show() calls should be allowed")
    
    def test_polyval_with_show_integration(self):
        """Test integration between polyval and show functions."""
        payroll = self.bball_data['Payroll']
        winpct = self.bball_data['WinPct']
        
        # This should work without errors
        p = np.polyfit(payroll, winpct, 1)
        fitted_values = np.polyval(p, payroll)
        
        # Verify fitted values are reasonable
        self.assertEqual(len(fitted_values), len(payroll))
        self.assertTrue(all(isinstance(val, (int, float, np.number)) for val in fitted_values))
        
        # This integration should work with plt.show()
        plt.plot(payroll, fitted_values, 'g-')
        # Note: not calling show() here to avoid display during testing


if __name__ == '__main__':
    unittest.main()