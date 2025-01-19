import { createTheme, alpha } from '@mui/material/styles';

// Google цвета
const google = {
  blue: '#4285F4',    // Google Blue
  green: '#0F9D58',   // Google Green
  yellow: '#F4B400',  // Google Yellow
  red: '#DB4437',     // Google Red
};

// Производные цвета
const derived = {
  lightBlue: alpha(google.blue, 0.1),
  lightGreen: alpha(google.green, 0.1),
  lightYellow: alpha(google.yellow, 0.1),
  lightRed: alpha(google.red, 0.1),
};

// Градиенты в стиле Google
const gradients = {
  primary: `linear-gradient(45deg, ${google.blue}, ${alpha(google.blue, 0.8)})`,
  secondary: `linear-gradient(45deg, ${google.red}, ${alpha(google.red, 0.9)})`,
  success: `linear-gradient(45deg, ${google.green}, ${alpha(google.green, 0.9)})`,
  warning: `linear-gradient(45deg, ${google.yellow}, ${alpha(google.yellow, 0.9)})`,
  multicolor: `linear-gradient(45deg, ${google.blue}, ${google.red}, ${google.yellow}, ${google.green})`,
};

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: google.blue,
      light: alpha(google.blue, 0.8),
      dark: alpha(google.blue, 1.2),
      contrastText: '#ffffff',
    },
    secondary: {
      main: google.red,
      light: alpha(google.red, 0.8),
      dark: alpha(google.red, 1.2),
      contrastText: '#ffffff',
    },
    success: {
      main: google.green,
      light: alpha(google.green, 0.8),
      dark: alpha(google.green, 1.2),
      contrastText: '#ffffff',
    },
    warning: {
      main: google.yellow,
      light: alpha(google.yellow, 0.8),
      dark: alpha(google.yellow, 1.2),
      contrastText: '#ffffff',
    },
    error: {
      main: google.red,
      light: alpha(google.red, 0.8),
      dark: alpha(google.red, 1.2),
      contrastText: '#ffffff',
    },
    background: {
      default: '#FFFFFF',
      paper: '#FFFFFF',
    },
    text: {
      primary: '#202124',
      secondary: '#5F6368',
    },
    divider: alpha(google.blue, 0.12),
    action: {
      active: alpha(google.blue, 0.7),
      hover: alpha(google.blue, 0.08),
      selected: alpha(google.blue, 0.12),
      disabled: alpha('#202124', 0.26),
      disabledBackground: alpha('#202124', 0.12),
    },
  },
  typography: {
    fontFamily: '"Google Sans", "Roboto", "Arial", sans-serif',
    h1: {
      fontSize: '3.5rem',
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.01562em',
      background: gradients.multicolor,
      WebkitBackgroundClip: 'text',
      WebkitTextFillColor: 'transparent',
      backgroundSize: '300% 300%',
      animation: 'gradient-shift 8s ease infinite',
    },
    h2: {
      fontSize: '2.75rem',
      fontWeight: 700,
      lineHeight: 1.2,
      letterSpacing: '-0.00833em',
      color: google.blue,
    },
    h3: {
      fontSize: '2.25rem',
      fontWeight: 600,
      lineHeight: 1.2,
      letterSpacing: '0em',
      color: google.red,
    },
    h4: {
      fontSize: '1.75rem',
      fontWeight: 600,
      lineHeight: 1.2,
      letterSpacing: '0.00735em',
      color: google.green,
    },
    h5: {
      fontSize: '1.5rem',
      fontWeight: 600,
      lineHeight: 1.2,
      letterSpacing: '0em',
      color: google.yellow,
    },
    h6: {
      fontSize: '1.25rem',
      fontWeight: 600,
      lineHeight: 1.2,
      letterSpacing: '0.0075em',
      color: google.blue,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: `
        @keyframes gradient-shift {
          0% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
          100% {
            background-position: 0% 50%;
          }
        }
      `,
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          textTransform: 'none',
          fontWeight: 500,
          padding: '8px 24px',
          boxShadow: 'none',
          '&:hover': {
            boxShadow: `0 1px 2px 0 ${alpha('#202124', 0.3)}`,
            transform: 'translateY(-1px)',
          },
          transition: 'all 0.2s ease-in-out',
        },
        contained: {
          '&:hover': {
            boxShadow: `0 1px 3px 0 ${alpha('#202124', 0.3)}`,
          },
        },
        containedPrimary: {
          background: gradients.primary,
          '&:hover': {
            background: gradients.primary,
            opacity: 0.9,
          },
        },
        containedSecondary: {
          background: gradients.secondary,
          '&:hover': {
            background: gradients.secondary,
            opacity: 0.9,
          },
        },
        outlined: {
          borderWidth: 1,
          '&:hover': {
            borderWidth: 1,
            backgroundColor: derived.lightBlue,
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          boxShadow: '0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15)',
          transition: 'all 0.2s ease-in-out',
          border: 'none',
          '&:hover': {
            transform: 'translateY(-2px)',
            boxShadow: '0 4px 8px 0 rgba(60,64,67,0.3), 0 2px 4px 0 rgba(60,64,67,0.15)',
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: alpha('#FFFFFF', 0.98),
          backdropFilter: 'blur(8px)',
          borderBottom: '1px solid rgba(0,0,0,0.12)',
          boxShadow: 'none',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 4,
            transition: 'all 0.2s ease-in-out',
            '&:hover': {
              boxShadow: `0 1px 2px 0 ${alpha('#202124', 0.2)}`,
            },
            '&.Mui-focused': {
              boxShadow: `0 1px 2px 0 ${alpha(google.blue, 0.2)}`,
            },
          },
        },
      },
    },
    MuiToggleButton: {
      styleOverrides: {
        root: {
          borderColor: alpha(google.blue, 0.2),
          transition: 'all 0.2s ease-in-out',
          '&.Mui-selected': {
            background: gradients.primary,
            color: '#ffffff',
            '&:hover': {
              background: gradients.primary,
              opacity: 0.9,
            },
          },
          '&:hover': {
            backgroundColor: derived.lightBlue,
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 16,
          '&.MuiChip-colorPrimary': {
            background: gradients.primary,
          },
          '&.MuiChip-colorSecondary': {
            background: gradients.secondary,
          },
          '&.MuiChip-colorSuccess': {
            background: gradients.success,
          },
          '&.MuiChip-colorWarning': {
            background: gradients.warning,
          },
        },
        label: {
          fontWeight: 500,
        },
      },
    },
    MuiListItemButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          '&.Mui-selected': {
            backgroundColor: derived.lightBlue,
            '&:hover': {
              backgroundColor: derived.lightBlue,
            },
          },
          '&:hover': {
            backgroundColor: derived.lightBlue,
          },
        },
      },
    },
  },
});

export default theme;
