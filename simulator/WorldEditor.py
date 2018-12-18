import cv2
import numpy as np
import os
from util.World import World
from util.LaneMarking import LaneMarking
from util.CurvedLaneMarking import CurvedLaneMarking
from util.TrafficLight import TrafficLight
from util.Camera import Camera
from util.Vehicle import Vehicle

"""
Keys:
+ zoom in
- zoom out
P toggle orthographic/projective
Z increase delta (which moves the object)
X decrease delta (which moves the object)
TAB select next actor
SHIFT select previous actor
WASD moves the selected actor
QE rotates the selected actor
Number keys: 1 LaneMarking
             2 TrafficLight
             3 CurvedLaneMarking
             4 Vehicle
~ Delete selected actor
C select camera immediately
"""


class WorldEditor:

    def __init__(self):
        cv2.namedWindow("Editor")
        cv2.setMouseCallback("Editor", self.mouse_listener)

        self.world = World()
        if os.path.exists(self.world.save_path):
            self.world = self.world.load_world()
            self.camera = self.world.get_camera_from_actors()
        else:
            self.camera = Camera()
            self.world.actors.append(LaneMarking())
            self.world.actors.append(self.camera)

        self.selected_index = -1
        self.selected_actor = None


    def mouse_listener(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            print (event)
            pass
        elif event == cv2.EVENT_LBUTTONUP:
            print (event)
            pass

    def edit(self):
        image = np.zeros((480, 640, 3), np.uint8)

        while True:
            image = self.world.render(image=image, C=self.camera)
            cv2.imshow("Editor", image)
            key = cv2.waitKey(33)
            self.interpret_key(key)
            if self.selected_actor != None:
                self.selected_actor.interpret_key(key)

    def interpret_key(self, key):
        if key == 9  or key == 49:
            self.select_actor(key)
        if key in [49, 50, 51, 52]:
            self.add_actor(key)
        if key == 13:
            self.world.save_world(overwrite=True)
        if key == 96:
            self.delete_selected_actor()
        if key == 99:
            self.select_camera_immediately()

        if key != -1: print ("Pressed key ", key)
        # if key == 112:
        #     self.camera.toggle_projection()

    def select_camera_immediately(self):
        if self.selected_actor != None:
            self.selected_actor.set_inactive()
        self.selected_actor = self.camera
        self.selected_actor.set_active()
        #keep the current index. do not change it

    def delete_selected_actor(self):
        if self.selected_actor != None and type(self.selected_actor) is not Camera:
            self.world.actors.remove(self.selected_actor)
            self.selected_index = 0

    def add_actor(self, key):
        if self.selected_actor != None:
            self.selected_actor.set_inactive()
        self.selected_index = len(self.world.actors) # we do that because we are adding one more actor at the end

        x, y, z, roll, yaw, pitch = self.camera.get_transform()
        new_actor = None
        if key == 49:
            new_actor = LaneMarking()
        if key == 50:
            new_actor = TrafficLight()
        if key ==51:
            new_actor = CurvedLaneMarking(arc_degree = 60, radius =300)
        if key == 52:
            new_actor = Vehicle()

        new_actor.set_transform(x = x, y = 0, z = z)
        self.world.actors.append(new_actor)
        self.selected_actor = new_actor
        self.selected_actor.set_active()

    def select_actor(self, key):
        if self.selected_actor != None:
            self.selected_actor.set_inactive()
        if key == 9:
            self.selected_index+=1
            if self.selected_index > len(self.world.actors)-1: self.selected_index = 0
            self.selected_actor = self.world.actors[self.selected_index]
        if key == 49:
            self.selected_index-=1
            if self.selected_index < 0: self.selected_index = len(self.world.actors) -1
            self.selected_actor = self.world.actors[self.selected_index]
        self.selected_actor.set_active()

if __name__ =="__main__":
    worldEditor = WorldEditor()
    worldEditor.edit()



