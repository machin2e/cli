import os
import re
import logging

import api
import git
import util

def assemble(component_identifiers, output_file=None):
    """
    Creates a YAML file describing the interfaces between the specified components.

    Parameters
    ----------
    component_identifiers : list of str
        List of *component identifier* strings used to search for corresponding
        *component files* in the form ``['identifier1', 'identifier2',
        'identifier3']``.
    output_file : str
        The file path where the output of the assembly process should be
        written.
        --output <filename> (optional) specifies output file for port config

    Examples
    --------
    gesso compose --component raspberry-pi-3 --component ir-rangefinder --component generic-servo
    gesso compose --component raspberry-pi-3 \
                    --component ir-rangefinder \
                    --component generic-servo \
                    --component generic-servo \
                    --output system.yaml

    Notes
    -----
    The arguments are essentially shorthand for filenames that match a specific format for models.
    First searches local folder, then model folder, fail to asking to create it (interactively create a device on the CLI with Gesso).
    """

    logger = util.logger(__name__, exclude_prefix=True)
    logger.info('%s' % component_identifiers)

    valid, invalid = validate_identifiers(component_identifiers)
    logger.info("VALID: %s" % valid)
    logger.info("INVALID: %s" % invalid)

    component_paths = find_component_files(component_identifiers)
    logger.info('%s' % component_paths)
    print "Found components."

    components = api.Component.open(component_paths)
    logger.info('%s' % components)
    print "Loaded component models."

    automatically_compose = raw_input(
        "Automatically compose the components? (Y/n):")

    paths = api.Component.compose(components)

def validate_identifiers(identifiers):
    """
    Returns a ``list`` that contains two elements. The first element is a
    ``list`` of the valid identifiers in ``identifiers`` and the second element
    is the complementary ``list`` of invalid identifiers in ``identifiers``.
    """

    # Prepare and compile regular expressions to validate model identifier tokens.
    # Matches strings such as:
    # - without semantic version: "gesso", "arduino", "raspberry-pi-3
    # - with semantic version: "gesso-3", "gesso-3.0", "gesso-3.0.0"
    generic_component_identifier_pattern = re.compile(
        r'^[0-9a-zA-Z_-]+(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}(\.(yaml)){0,1}$')

    # Matches strings such as:
    # - "gesso/ir-rangefinder"
    # - "gesso/raspberry-pi-3"
    component_github_pattern = re.compile(r'^[A-Za-z0-9-_]+\/[A-Za-z0-9-_]+$')

    # Validate the requested component identifiers. Halt and show error if
    # any are not in a valid format.
    logger = util.logger(__name__, exclude_prefix=True)
    logger.info('Requested components (by identifier):')

    valid = []
    invalid = []
    for component_identifier in identifiers:
        if generic_component_identifier_pattern.match(component_identifier) or component_github_pattern.match(component_identifier):
            logger.info('\tvalid\t%s' % component_identifier)
            valid.append(component_identifier)
        else:
            logger.info('\tinvalid\t%s' % component_identifier)
            invalid.append(component_identifier)
    logger.info('\n')

    return [valid, invalid]

def find_component_files(component_identifiers):
    """
    Accepts list of component identifiers (such as names), filenames, GitHub 
    repositories (e.g., "gesso/raspberry-pi-3"), or file paths.

    Returns dictionary with keys from input and values as the associated 
    component paths.
    """
    logger = util.logger(__name__, exclude_prefix=True)

    # Matches strings such as:
    # - "gesso/ir-rangefinder"
    # - "gesso/raspberry-pi-3"
    component_github_pattern = re.compile(r'^[A-Za-z0-9-_]+\/[A-Za-z0-9-_]+$')

    logger.info('Component File Paths:')
    component_file_paths = {}
    path_list = []
    current_dir = util.get_current_dir()
    for component_identifier in component_identifiers:

        # Prepare and compile regular expressions for validating and identifying a model file.
        component_path_pattern = re.compile(
            r'^%s(-(?:(\d+)\.)?(?:(\d+)\.)?(\*|\d+)){0,1}\.(yaml)$' % component_identifier)

        # Search local directory for YAML file (based on input argument)
        if component_identifier not in component_file_paths:
            for file_name in util.get_file_list():
                if component_path_pattern.match(file_name) is not None:
                    component_file_paths[component_identifier] = '%s/%s' % (
                        current_dir, file_name)

        # Search library's data/models folder
        if component_identifier not in component_file_paths:
            data_dir = util.get_data_dir()
            for file_name in util.get_file_list(data_dir):
                if component_path_pattern.match(file_name) is not None:
                    component_file_paths[component_identifier] = '%s/%s' % (
                        data_dir, file_name)

        # Check for GitHub repository identifier
        if component_identifier not in component_file_paths:
            # TODO: Write function to load model file from a GitHub repository specified with format 'username/repo'
            if component_github_pattern.match(component_identifier) is not None:
                logger.info('Cloning %s/%s to %s/%s/%s' % (username,
                                                           repository, '.gesso/components', username, repository))
                username, repository = component_identifier.split('/')
                git.clone_github_repository(username, repository)

        # No component file was found for the specified identifer, so halt and show an error.
        # if component_identifier not in component_file_paths:
            # print "No component file found for '%s'." % component_identifier
            # # TODO: Log error/warning/info
            # None

    for component_identifier in component_identifiers:
        path_list.append(component_file_paths[component_identifier])

    for component_identifier in component_identifiers:
        logger.info('\t%s => Found component file: %s' % (
            component_identifier, component_file_paths[component_identifier]))
    logger.info('')

    return path_list

def select_compatible_port(port, compatible_port_list):
    """
    Selects a port from `compatible_port_list` to which `port` will be connected with a path.
    """
    None

if __name__ == "__main__":
    assemble()
