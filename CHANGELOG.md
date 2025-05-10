# CHANGELOG

## 2.3.2 (2025-05-10)

### Major Features Added

- Added `dictConfig` function: Configuration feature compatible with standard logging.config.dictConfig
- Added `yaml_config` function: Feature to load configuration from YAML files
- Added `fileConfig` function: Configuration feature compatible with standard logging.config.fileConfig
- Improved color setting flexibility: Feature to configure colors in dictConfig format
- Automatic environment variable loading: Automatically applies settings when the module is loaded

### Improvements

- Enhanced compatibility with standard logging library: Unified configuration methods
- Maintained backward compatibility with existing color setting methods

### Deprecated Features

- Changed `NO_COLOR` environment variable to deprecated: Recommended to use `LOGKISS_DISABLE_COLOR` instead

### Removed Features

- Removed `setup` function: To improve compatibility with standard logging library
- Removed `setup_from_yaml` function: Replaced with `yaml_config` function
- Removed `setup_from_env` function: Replaced with automatic environment variable loading feature

## 2.3.0 (2025-04-30)

### Major Features Added

- Modified `basicConfig` function: Ensured compatibility with standard logging module
- Published `setup` function: Simplified automatic detection and application of configuration files
- Added module API tests: Verified compatibility with standard logging module
- Added support for `NO_COLOR` environment variable: Implemented as an industry standard environment variable

### Improvements

- Improved code quality: Removed unused imports, enhanced exception handling
- Added encoding specification when opening files
- Fixed built-in name overrides
- Enhanced test environment: Added environment variable tests

### Changes in 2.2.6

- Modified `basicConfig` function: Ensured compatibility with standard logging module
- Published `setup` function: Simplified automatic detection and application of configuration files
- Added module API tests: Verified compatibility with standard logging module

## 2.2.5 (2025-04-30)

### Improvements

- Added support for `NO_COLOR` environment variable
  - As an industry standard environment variable, disables color output just by existing regardless of value
- Fully implemented environment variable tests
- Improved code quality:
  - Removed unused imports
  - Added encoding specification when opening files
  - Changed general exception catches to specific exceptions
  - Fixed built-in name overrides

## 2.2.4 (2025-04-15)

### Improvements

- Enhanced support for color configuration files
- Added log level customization feature
- Optimized performance

## 2.2.3 (2025-04-01)

### Bug Fixes

- Fixed color display issues in Windows environments
- Resolved conflict issues when using multiple loggers

### Improvements

- Enhanced multilingual support for documentation
- Extended search paths for configuration files
