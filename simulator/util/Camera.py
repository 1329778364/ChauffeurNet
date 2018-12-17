from .Actor import Actor
import numpy as np

class Camera(Actor):
    def __init__(self, cam_config = None):
        """
        :param cam_config: dictionary containing image width, image height, focal length in centimeters, pixel_width in centimeters
        :param x, y, z, roll, yaw, pitch in world coordinates
        T = transformation matrix in world coordinates R * t
        """
        super().__init__()
        if cam_config == None:
            self.cam_config = {"img_w": 640, "img_h": 480, "f_cm": 0.238, "pixel_width_cm": 0.0003}
        else:
            self.cam_config = cam_config
        self.K = self.create_K(self.cam_config)
        self.set_transform(x=0, y=-1000, z=0, roll=0, yaw=0, pitch=-90)

        self.project = self.project_perspective

    def create_cammera_matrix(self, T, K):
        """
        Create camera matrix. it will be a 4x4 matrix
        T defines the camera rotation and translation in world coordinate system.
        we need a matrix that will transform points from world coordinates to camera coordinates in order to project them
        that matrix will do the inverse of translation followed by inverse of rotation followed by camera matrix
        """
        C = K.dot(np.linalg.inv(T)[:3,:])
        return C

    def create_K(self, cam_config):
        img_w = cam_config["img_w"]
        img_h = cam_config["img_h"]
        f_cm  = cam_config["f_cm"]
        pixel_width = cam_config["pixel_width_cm"]

        fx = f_cm / pixel_width
        fy = f_cm / pixel_width
        cx = img_w / 2
        cy = img_h / 2

        K = np.eye(3)
        K[0,0] = fx
        K[1,1] = fy
        K[0,2] = cx
        K[1,2] = cy

        return K

    #@Override
    def set_transform(self, x = 0,y = 0,z = 0,roll = 0, yaw = 0, pitch = 0):
        super(Camera, self).set_transform(x ,y ,z ,roll , yaw , pitch )
        self.C = self.create_cammera_matrix(self.T, self.K)

    def project_ortographic(self, vertices):
        homogeneous_vertices = self.C.dot(vertices)
        homogeneous_vertices /= homogeneous_vertices[2, :]
        homogeneous_vertices += self.center
        v = homogeneous_vertices.astype(np.int32)
        x = v[0, :]
        y = v[1, :]
        return x, y

    def project_perspective(self, vertices):
        #vertices have shape 4xN.
        #C is 3x4 matrix
        homogeneous_vertices = self.C.dot(vertices)
        # divide u, v by z
        projected_vertices = homogeneous_vertices / homogeneous_vertices[2, :]
        v = projected_vertices.astype(np.int32)
        x = v[0, :]
        y = v[1, :]
        return x, y

    def toggle_projection(self):
        if self.project == self.project_perspective:
            self.K = np.eye(3)
            self.center = np.array([[self.cam_config["img_w"] / 2],
                                    [self.cam_config["img_h"] / 2],
                                    [0.0]])
            self.project = self.project_ortographic
        else:
            self.K = self.create_K(self.cam_config)
            self.project = self.project_perspective
        self.C = self.create_cammera_matrix(self.T, self.K)

    #@Override
    def set_active(self):
        print ("Reached camera. No action for color")