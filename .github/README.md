# GitHub Automation

This directory contains GitHub Actions workflows and configuration files for the Ayra Trust Registry Resources repository.

## Workflows

### Docker Build and Test

- [docker-build-test.yml](./workflows/docker-build-test.yml) - Builds and tests the Docker containers for the playground environment.

### Render Specifications

- [render-specs.yaml](./workflows/render-specs.yaml) - Renders the specification documents into the distribution formats in the `dist` directory.

## Usage

These workflows run automatically on GitHub when:

- New code is pushed to the repository
- Pull requests are created or updated
- Scheduled events occur (if configured)

## Local Testing

If you want to test the workflows locally before pushing to GitHub:

1. Install [act](https://github.com/nektos/act)
2. Run a workflow locally:
   ```bash
   act -W .github/workflows/docker-build-test.yml
   ```

## Adding New Workflows

When adding new workflows, please:

1. Ensure they follow the repository's security and access requirements
2. Document their purpose in this README
3. Include appropriate triggers and conditions
4. Test them thoroughly before merging to the main branch
