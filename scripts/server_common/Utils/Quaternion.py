# -*- coding: utf-8 -*-
import math
import Math

sin = math.sin
cos = math.cos
RadToDeg = 180 / math.pi
DegToRad = math.pi / 180

class Quaternion():
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.vector = [x,y,z,w]
        
    def euler(x,y,z):
        pitchRad = x * DegToRad / 2
        yawRad = y * DegToRad / 2
        rollRad = z * DegToRad / 2

        sinPitchHalf = sin(pitchRad)
        cosPitchHalf = cos(pitchRad)
        sinYawHalf = sin(yawRad)
        cosYawHalf = cos(yawRad)
        sinRollHalf = sin(rollRad)
        cosRollHalf = cos(rollRad)

        qw = cosYawHalf * cosPitchHalf * cosRollHalf + sinYawHalf * sinPitchHalf * sinRollHalf
        qx = cosYawHalf * sinPitchHalf * cosRollHalf + sinYawHalf * cosPitchHalf * sinRollHalf
        qy = sinYawHalf * cosPitchHalf * cosRollHalf - cosYawHalf * sinPitchHalf * sinRollHalf
        qz = cosYawHalf * cosPitchHalf * sinRollHalf - sinYawHalf * sinPitchHalf * cosRollHalf
        return Quaternion(qx,qy,qz,qw)
    
    def multiVec3(self, v):
        x = v.x
        y = v.y
        z = v.z
        num = self.vector[0] * 2
        num2 = self.vector[1] * 2
        num3 = self.vector[2] * 2
        num4 = self.vector[0] * num
        num5 = self.vector[1] * num2
        num6 = self.vector[2] * num3
        num7 = self.vector[0] * num2
        num8 = self.vector[0] * num3
        num9 = self.vector[1] * num3
        num10 = self.vector[3] * num
        num11 = self.vector[3] * num2
        num12 = self.vector[3] * num3
        rx = (((1 - (num5 + num6)) * x) + ((num7 - num12) * y)) + ((num8 + num11) * z)
        ry = (((num7 + num12) * x) + ((1 - (num4 + num6)) * y)) + ((num9 - num10) * z)
        rz = (((num8 - num11) * x) + ((num9 + num10) * y)) + ((1 - (num4 + num5)) * z)
        return Math.Vector3(rx, ry, rz)
        
    def axisAngle(axis, angle):
        axis.normalise()
        rad = angle * DegToRad / 2
        s = sin(rad)
        w = cos(rad)
        x = axis.x * s
        y = axis.y * s
        z = axis.z * s
        return Quaternion(x, y, z, w)
        
