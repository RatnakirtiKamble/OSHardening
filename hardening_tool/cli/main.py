import argparse
import sys

def main():
    # 1. Top-level parser for the 'hardtack' command
    parser = argparse.ArgumentParser(
        prog='hardtack',
        description='A command-line tool to manage OS hardening policies on a Local Area Network (LAN).'
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Provides more detailed, step-by-step output.')
    parser.add_argument('-q', '--quiet', action='store_true', help='Suppresses all output except for critical errors.')
    
    # Create subparsers for main command groups (e.g., 'device', 'policy')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # =================================================================
    # 'init' Command
    # =================================================================
    parser_init = subparsers.add_parser('init', help='Scans the LAN and initializes the monitoring system.')
    parser_init.set_defaults(func=handle_init)

    # =================================================================
    # 'device' Command Group
    # =================================================================
    parser_device = subparsers.add_parser('device', help='Manage devices on the network.')
    device_subparsers = parser_device.add_subparsers(dest='device_command', help='Device commands')

    # 'device list' command
    parser_device_list = device_subparsers.add_parser('list', help='Lists all managed devices.')
    parser_device_list.add_argument('--status', choices=['online', 'offline'], help='Filter by device status.')
    parser_device_list.add_argument('--policy', help='Filter by assigned policy level.')
    parser_device_list.set_defaults(func=handle_device_list)

    # 'device add' command
    parser_device_add = device_subparsers.add_parser('add', help='Adds a new device.')
    parser_device_add.add_argument('hostname', help='The hostname of the device.')
    parser_device_add.add_argument('--ip', required=True, help='The IP address of the device.')
    parser_device_add.add_argument('-r', '--read-file', help='Adds multiple devices in bulk from a text file.')
    parser_device_add.set_defaults(func=handle_device_add)

    # 'device remove' command
    parser_device_remove = device_subparsers.add_parser('remove', help='Removes a device.')
    parser_device_remove.add_argument('hostname', help='The hostname or IP of the device to remove.')
    parser_device_remove.set_defaults(func=handle_device_remove)
    
    # 'device ping' command
    parser_device_ping = device_subparsers.add_parser('ping', help='Pings a device to check connectivity.')
    parser_device_ping.add_argument('hostname', help='The hostname or IP of the device to ping.')
    parser_device_ping.set_defaults(func=handle_device_ping)

    # =================================================================
    # 'policy' Command Group
    # =================================================================
    parser_policy = subparsers.add_parser('policy', help='Manage security policies.')
    policy_subparsers = parser_policy.add_subparsers(dest='policy_command', help='Policy commands')

    # 'policy create' command
    parser_policy_create = policy_subparsers.add_parser('create', help='Creates a new policy level.')
    parser_policy_create.add_argument('level_name', help='The name for the new policy level.')
    parser_policy_create.set_defaults(func=handle_policy_create)
    
    # 'policy assign' command
    parser_policy_assign = policy_subparsers.add_parser('assign', help='Assigns a policy to a device.')
    parser_policy_assign.add_argument('level_name', help='The policy level to assign.')
    group = parser_policy_assign.add_mutually_exclusive_group(required=True)
    group.add_argument('--device', help='The specific device to assign the policy to.')
    group.add_argument('--all', action='store_true', help='Assign the policy to all devices.')
    parser_policy_assign.set_defaults(func=handle_policy_assign)
    
    # 'policy list' command
    parser_policy_list = policy_subparsers.add_parser('list', help='Lists all available policy levels.')
    parser_policy_list.set_defaults(func=handle_policy_list)

    # =================================================================
    # 'rule' Command Group
    # =================================================================
    parser_rule = subparsers.add_parser('rule', help='Manage rules within policies.')
    rule_subparsers = parser_rule.add_subparsers(dest='rule_command', help='Rule commands')
    
    # 'rule modify' command
    parser_rule_modify = rule_subparsers.add_parser('modify', help='Modifies a rule in a policy.')
    parser_rule_modify.add_argument('rule_id', help='The ID of the rule to modify (e.g., sshd.permit_root_login).')
    parser_rule_modify.add_argument('--level', required=True, help='The policy level to modify.')
    parser_rule_modify.add_argument('--set', required=True, choices=['true', 'false'], help='Set the rule to true or false.')
    parser_rule_modify.set_defaults(func=handle_rule_modify)

    # =================================================================
    # 'status' Command
    # =================================================================
    parser_status = subparsers.add_parser('status', help='Check compliance status of devices.')
    parser_status.add_argument('--device', help='Check status of a specific device.')
    parser_status.add_argument('--show-failed', action='store_true', help='Only show failing rules.')
    parser_status.set_defaults(func=handle_status)
    
    # =================================================================
    # 'enforce' command
    # =================================================================
    parser_enforce = subparsers.add_parser('enforce', help='Enforce policies on a device.')
    parser_enforce.add_argument('hostname', help='The device to enforce policy on.')
    parser_enforce.add_argument('--dry-run', action='store_true', help='Simulate changes without applying them.')
    parser_enforce.set_defaults(func=handle_enforce)


    # Parse the arguments
    # If no command is given, print help
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()

    # Call the function associated with the command
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # If a command group was called without a subcommand (e.g., 'hardtack device')
        if args.command:
            # Get the subparser for the command and print its help
            subparser_action = next((action for action in parser._actions if isinstance(action, argparse._SubParsersAction)), None)
            if subparser_action:
                subparser = subparser_action.choices.get(args.command)
                if subparser:
                    subparser.print_help()
                    sys.exit(1)
        parser.print_help()


# =================================================================
# Handler Functions (Mock Logic)
# =================================================================

def handle_init(args):
    print("ACTION: Initializing hardtack...")
    print("-> Scanning network for devices...")
    print("-> Initialization complete.")

def handle_device_list(args):
    print(f"ACTION: Listing devices...")
    if args.status:
        print(f"-> Filtering by status: {args.status}")
    if args.policy:
        print(f"-> Filtering by policy: {args.policy}")

def handle_device_add(args):
    if args.read_file:
        print(f"ACTION: Adding devices in bulk from file: {args.read_file}")
    else:
        print(f"ACTION: Adding device '{args.hostname}' with IP '{args.ip}'...")

def handle_device_remove(args):
    print(f"ACTION: Removing device '{args.hostname}'...")

def handle_device_ping(args):
    print(f"ACTION: Pinging device '{args.hostname}'...")

def handle_policy_create(args):
    print(f"ACTION: Creating new policy level '{args.level_name}'...")

def handle_policy_assign(args):
    target = f"device '{args.device}'" if args.device else "all devices"
    print(f"ACTION: Assigning policy '{args.level_name}' to {target}...")

def handle_policy_list(args):
    print("ACTION: Listing available policies...")
    print("-> Strict\n-> Medium\n-> Light")

def handle_rule_modify(args):
    print(f"ACTION: Modifying rule in policy '{args.level}'...")
    print(f"-> Setting rule '{args.rule_id}' to '{args.set}'")

def handle_status(args):
    if args.device:
        print(f"ACTION: Checking detailed status for device '{args.device}'...")
    else:
        print(f"ACTION: Checking compliance status for all devices...")
    if args.show_failed:
        print("-> Displaying only failed rules.")

def handle_enforce(args):
    print(f"ACTION: Enforcing policy on '{args.hostname}'...")
    if args.dry_run:
        print("-> This is a DRY RUN. No changes will be made.")
    else:
        print("-> Applying changes...")

if __name__ == '__main__':
    main()
