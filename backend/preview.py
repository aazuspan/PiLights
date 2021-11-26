import argparse
import os
import logging

def preview(name):
    """Run a synchronous visualization preview."""
    from backend.Controller import Controller
    
    controller = Controller()
    
    vis_class = controller.get_vis_by_name(name)
    logging.info(f"Previewing {name}")
    
    controller.current_vis = vis_class(pixels=controller.pixels)
    
    try:
        controller.run_vis()
    except KeyboardInterrupt:
        controller.clear_pixels()
    

if __name__ == "__main__":
    # Prevent the controller from searching for wemos
    os.environ["ignore_wemos"] = "1"
    
    parser = argparse.ArgumentParser(description="Preview a visualization.")
    parser.add_argument('-n', '--name', help="Visualization name to run")
    args = parser.parse_args()
    name = args.name
    
    preview(name)
