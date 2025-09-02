import unittest
import matplotlib.pyplot as plt
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import io


class TestPlottingFunctions(unittest.TestCase):
    """Test suite for matplotlib plotting functions to ensure correct usage."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Create sample data similar to what might be in the notebook
        self.sample_payroll = np.array([50, 100, 150, 200, 250])
        self.sample_winpct = np.array([0.3, 0.5, 0.6, 0.7, 0.8])
        
    def tearDown(self):
        """Clean up after each test method."""
        plt.close('all')
    
    @patch('matplotlib.pyplot.show')
    def test_valid_plt_show_call(self, mock_show):
        """Test that plt.show() is called correctly without errors."""
        # Create a simple plot
        plt.plot(self.sample_payroll, self.sample_winpct)
        plt.show()
        
        # Verify show was called once
        mock_show.assert_called_once()
    
    def test_plt_show2_does_not_exist(self):
        """Test that plt.show2() does not exist and raises AttributeError."""
        with self.assertRaises(AttributeError):
            plt.show2()
    
    def test_plt_show3_does_not_exist(self):
        """Test that plt.show3() does not exist and raises AttributeError."""
        with self.assertRaises(AttributeError):
            plt.show3()
    
    @patch('matplotlib.pyplot.show')
    def test_polyfit_plot_sequence(self, mock_show):
        """Test the complete plotting sequence with polyfit as shown in the diff context."""
        # Simulate the code from the notebook context
        p = np.polyfit(self.sample_payroll, self.sample_winpct, 1)
        plt.plot(self.sample_payroll, np.polyval(p, self.sample_payroll), 'g-')
        plt.show()
        
        # Verify show was called
        mock_show.assert_called_once()
    
    def test_matplotlib_show_function_exists(self):
        """Test that plt.show is a valid callable function."""
        self.assertTrue(hasattr(plt, 'show'))
        self.assertTrue(callable(getattr(plt, 'show')))
    
    def test_invalid_show_methods_do_not_exist(self):
        """Test that invalid show methods do not exist in matplotlib.pyplot."""
        invalid_methods = ['show2', 'show3', 'show4', 'show_extra']
        
        for method in invalid_methods:
            self.assertFalse(hasattr(plt, method), 
                            f"plt.{method} should not exist in matplotlib.pyplot")


if __name__ == '__main__':
    unittest.main()