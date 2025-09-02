import unittest
import re
import ast
import sys
from unittest.mock import patch, mock_open


class TestNotebookCodeValidation(unittest.TestCase):
    """Test suite for validating notebook code patterns and preventing common errors."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Sample notebook-like code that should be valid
        self.valid_code_block = '''
        p=polyfit(bball.Payroll,bball.WinPct,1)
        plt.plot(bball.Payroll, polyval(p,bball.Payroll),'g-')
        plt.show()
        '''
        
        # Sample code with invalid show calls (like what was removed)
        self.invalid_code_block = '''
        p=polyfit(bball.Payroll,bball.WinPct,1)
        plt.plot(bball.Payroll, polyval(p,bball.Payroll),'g-')
        plt.show()
        plt.show2()
        plt.show3()
        '''
    
    def test_detect_invalid_plt_show_calls(self):
        """Test detection of invalid plt.show variants in code."""
        # Pattern to detect invalid show calls
        invalid_show_pattern = r'plt\.show[0-9]+\(\)'
        
        # Should not find invalid patterns in valid code
        valid_matches = re.findall(invalid_show_pattern, self.valid_code_block)
        self.assertEqual(len(valid_matches), 0, 
                        "Valid code should not contain invalid plt.show variants")
        
        # Should find invalid patterns in invalid code
        invalid_matches = re.findall(invalid_show_pattern, self.invalid_code_block)
        self.assertEqual(len(invalid_matches), 2, 
                        "Should detect plt.show2() and plt.show3() as invalid")
        self.assertIn('plt.show2()', invalid_matches)
        self.assertIn('plt.show3()', invalid_matches)
    
    def test_valid_plt_show_pattern(self):
        """Test that valid plt.show() calls are preserved."""
        valid_show_pattern = r'plt\.show\(\)'
        
        # Should find valid plt.show() in both code blocks
        valid_matches_in_valid = re.findall(valid_show_pattern, self.valid_code_block)
        valid_matches_in_invalid = re.findall(valid_show_pattern, self.invalid_code_block)
        
        self.assertEqual(len(valid_matches_in_valid), 1)
        self.assertEqual(len(valid_matches_in_invalid), 1)
    
    def test_code_syntax_validation(self):
        """Test that code blocks have valid Python syntax after cleanup."""
        # Clean up the valid code block
        cleaned_valid = self.valid_code_block.strip()
        
        # Should be able to parse as valid Python
        try:
            ast.parse(cleaned_valid)
            syntax_valid = True
        except SyntaxError:
            syntax_valid = False
        
        self.assertTrue(syntax_valid, "Valid code block should have correct Python syntax")
    
    def test_removed_lines_validation(self):
        """Test validation of the specific lines that were removed in the diff."""
        removed_lines = ['"plt.show2()"', '"plt.show3()"']
        
        for line in removed_lines:
            # These lines should be identified as problematic
            # Strip quotes and check if it contains invalid function calls
            code_content = line.strip('"')
            self.assertRegex(code_content, r'plt\.show[0-9]+\(\)',
                           f"Line {line} should be identified as containing invalid matplotlib call")
    

if __name__ == '__main__':
    unittest.main()
