import argparse
import os
from string import Template
import shutil


def create_dashboard_files(args):
    # Create dash dir
    os.mkdir(args.dashboard)
    # create __init__.py for dashboard
    open('{}/__init__.py'.format(args.dashboard), 'w').close()
    # create the usual dirs
    for dashdir in ['templates', 'templatetags']:
        os.mkdir('{}/{}'.format(args.dashboard, dashdir))
    # create static dir
    os.makedirs('{0}/{1}/{0}'.format(args.dashboard, 'static'))
    # create dashboard.py
    with open('templates/dashboard/dashboard.py.template', 'r') as file_read:
        template = Template(file_read.read())
        with open('{}/dashboard.py'.format(args.dashboard), 'w') as file_write:
            file_write.write(
                template.substitute(
                    DASHBOARD_SLUG=args.dashboard_slug or args.dashboard.lower(),
                    DASHBOARD_NAME=args.dashboard.capitalize(),
                    GROUP_PANEL_NAME=args.groupname,
                    PANEL_SLUG=args.panel_slug or args.panel.lower(),
                    PANEL_NAME=args.panel.capitalize())
            )


def create_panel_files(args):
    # create panel dir
    os.mkdir('{}/{}'.format(args.dashboard, args.panel))
    # create __init__.py for panel
    open('{}/{}/__init__.py'.format(args.dashboard, args.panel), 'w').close()
    # create template dirs
    os.makedirs('{}/templates/{}'.format(args.dashboard, args.panel))
    # copy index.html
    shutil.copyfile(
        'templates/panel/index.html.template',
        '{}/templates/{}/index.html'.format(args.dashboard, args.panel)
    )

    # copy urls.py
    shutil.copyfile(
        'templates/panel/urls.py.template',
        '{}/{}/urls.py'.format(args.dashboard, args.panel)
    )

    # create panel.py
    with open('templates/panel/panel.py.template', 'r') as file_read:
        template = Template(file_read.read())
        with open('{}/{}/panel.py'.format(args.dashboard, args.panel), 'w') as file_write:
            file_write.write(
                template.substitute(
                    DASHBOARD_NAME=args.dashboard.capitalize(),
                    PANEL_SLUG=args.panel_slug or args.panel.lower(),
                    PANEL_NAME=args.panel.capitalize()
                )
            )
    # create views.py
    with open('templates/panel/views.py.template', 'r') as file_read:
        template = Template(file_read.read())
        with open('{}/{}/views.py'.format(args.dashboard, args.panel), 'w') as file_write:
            file_write.write(
                template.substitute(
                    DASHBOARD_NAME=args.dashboard,
                    PANEL_NAME=args.panel
                )
            )


def create_root_files(args):
    # create setup.cfg
    with open('templates/setup.cfg.template', 'r') as file_read:
        template = Template(file_read.read())
        with open('setup.cfg', 'w') as file_write:
            file_write.write(template.substitute(DASHBOARD_NAME=args.dashboard))

    # create manage.py
    with open('templates/manage.py.template', 'r') as file_read:
        template = Template(file_read.read())
        with open('manage.py', 'w') as file_write:
            file_write.write(template.substitute(DASHBOARD_NAME=args.dashboard))


def create_enabled_file(args):
    os.mkdir('enabled')
    with open('templates/_55_dashboard.py.template', 'r') as file_read:
        template = Template(file_read.read())
        with open('enabled/_55_{}.py'.format(args.dashboard), 'w') as file_write:
            file_write.write(template.substitute(DASHBOARD_NAME=args.dashboard))


def cleanup(args):
    """If something fails, clean up"""
    shutil.rmtree(args.dashboard)
    shutil.rmtree('enabled')
    os.remove('setup.cfg')
    os.remove('manage.py')


def string_no_spaces(value):
    """Validate that there is no unwanted items in the user input"""
    if " " in value:
        raise argparse.ArgumentTypeError(
            "'{}' has spaces and they are not allowed".format(value)
        )
    return value


def check_dir_exists(args):
    if os.path.exists(args.dashboard):
        print("Directory already exists with that name")
        exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dashboard', help='Dashboard name',
                        type=string_no_spaces)
    parser.add_argument('panel', help='Panel name',
                        type=string_no_spaces)
    parser.add_argument('groupname', help='Group name',
                        type=string_no_spaces)
    parser.add_argument('--dashboard-slug',
                        help='Dashboard slug to use, defaults to the name',
                        type=string_no_spaces)
    parser.add_argument('--panel-slug',
                        help='Panel slug to use, defaults to the name',
                        type=string_no_spaces)
    args = parser.parse_args()

    check_dir_exists(args)

    try:
        create_dashboard_files(args)
        create_panel_files(args)
        create_root_files(args)
        create_enabled_file(args)
    except Exception:
        cleanup(args)
        raise


if __name__ == "__main__":
    main()
