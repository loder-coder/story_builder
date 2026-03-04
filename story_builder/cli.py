import argparse
import os
import json
import sys
from story_builder import Engine, StoryGraph, EngineState

def visualize_command(args):
    """Command for story graph visualization."""
    from story_builder.export.render import write_dot, render_dot_to_image, open_file

    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist.")
        sys.exit(2)

    try:
        with open(args.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error: Failed to parse JSON file: {e}")
        sys.exit(2)

    try:
        graph = StoryGraph(**data)
        
        # Paths logic
        base, _ = os.path.splitext(args.path)
        out_dot = f"{base}.dot"
        out_img = args.out or f"{base}.{args.format}"
        
        # 1. Output DOT
        write_dot(graph, out_dot)
        
        if args.dot_only:
            return

        # 2. Render to image
        success = render_dot_to_image(out_dot, out_img, format=args.format, engine=args.engine)
        
        if success:
            print(f"Successfully visualized to: {out_img}")
            if not args.no_open:
                open_file(out_img)
        else:
            print("\nHint: Only the .dot file was generated. To render it as an image, please:")
            print("  - pip install 'story-builder[viz]'")
            print("  - Ensure GraphViz system binaries are installed (http://graphviz.org)")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)

def play_command(args):
    """Command for playing through a story."""
    if not args.path:
        print("Error: path is required for play.")
        sys.exit(2)
        
    if not os.path.exists(args.path):
        print(f"Error: Story file '{args.path}' not found.")
        sys.exit(2)
        
    try:
        from story_builder.utils.loaders import load_graph
        story_graph = load_graph(args.path)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(2)
        
    engine = Engine(story_graph)
    
    # Start game
    state = EngineState(current_node_id=story_graph.start_node_id, variables={})
    
    print(f"\nStarting Adventure: {story_graph.metadata.get('title', 'Unknown')}")
    print("-" * 50)
    
    while True:
        node, triggers, _ = engine.run(state.current_node_id, state.variables)
        
        print(f"\nNode: {node.title}")
        print(f"Body: {node.body}")
        
        if not triggers:
            print("\n[GAME OVER] No choices left.")
            break
            
        print("\nAvailable Actions:")
        for i, t in enumerate(triggers, start=1):
            print(f"  {i}. {t}")
        
        try:
            choice = input("\n> ")
            if choice.lower() in ['exit', 'quit']:
                break
            
            # Check for numerical choice
            if choice.isdigit() and 0 < int(choice) <= len(triggers):
                selected_trigger = triggers[int(choice)-1]
            else:
                selected_trigger = choice
            
            # Process trigger
            engine.process_trigger(selected_trigger, state)
            
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.")

def main():
    parser = argparse.ArgumentParser(description="Story Builder Narrative Engine CLI")
    
    # Compatible with old usage (at least to some extent)
    # python -m story_builder.cli --load examples/minimal_story.json
    parser.add_argument("--load", type=str, help="Load an example story JSON (deprecated: use 'play' subcommand)")
    parser.add_argument("--play", action="store_true", help="Start a new adventure (deprecated: use 'play' subcommand)")

    subparsers = parser.add_subparsers(dest="subcommand", help="sub-command help")

    # Command: play
    play_parser = subparsers.add_parser("play", help="Play a story graph.")
    play_parser.add_argument("path", nargs="?", help="Path to the story JSON file.")

    # Command: visualize
    viz_parser = subparsers.add_parser("visualize", help="Visualize a story graph.")
    viz_parser.add_argument("path", help="Path to the story JSON file.")
    viz_parser.add_argument("--out", type=str, help="Output image path.")
    viz_parser.add_argument("--format", type=str, default="png", choices=["png", "svg"], help="Output format (default: png).")
    viz_parser.add_argument("--no-open", action="store_true", help="Do not auto-open the rendered image.")
    viz_parser.add_argument("--dot-only", action="store_true", help="Only generate the DOT file, skip rendering.")
    viz_parser.add_argument("--engine", type=str, default="dot", choices=["dot", "neato"], help="GraphViz layout engine (default: dot).")

    args = parser.parse_args()

    # Legacy support
    if args.load:
        args.path = args.load
        play_command(args)
        return

    if args.subcommand == "play":
        play_command(args)
    elif args.subcommand == "visualize":
        visualize_command(args)
    else:
        parser.print_help()
        sys.exit(0)

if __name__ == "__main__":
    main()
