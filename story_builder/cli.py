import argparse
import os
import json
from story_builder.core.graph import StoryGraph
from story_builder.core.executor import Engine
from story_builder.core.state import EngineState

def main():
    parser = argparse.ArgumentParser(description="Story Builder Narrative Engine CLI")
    parser.add_argument("--load", type=str, help="Load an example story JSON")
    parser.add_argument("--play", action="store_true", help="Start a new adventure")
    args = parser.parse_args()

    if args.load:
        if not os.path.exists(args.load):
            print(f"Error: Story file '{args.load}' not found.")
            return
            
        with open(args.load, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        story_graph = StoryGraph(**data)
        engine = Engine(story_graph)
        
        # Start game
        state = EngineState(current_node_id=story_graph.start_node_id, variables={})
        
        print(f"\n🚀 Starting Adventure: {story_graph.metadata.get('title', 'Unknown')}")
        print("-" * 50)
        
        while True:
            node, triggers, _ = engine.run(state.current_node_id, state.variables)
            
            print(f"\n📍 {node.title}")
            print(f"📝 {node.body}")
            
            if not triggers:
                print("\n[GAME OVER] No choices left.")
                break
                
            print("\n🔥 Available Actions:")
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
                print(f"\n❌ Error: {e}")
                print("Please try again.")

if __name__ == "__main__":
    main()
