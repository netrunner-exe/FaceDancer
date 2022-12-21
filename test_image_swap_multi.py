# -*- coding: utf-8 -*-
# @Author: netrunner-exe
# @Date:   2022-12-21 12:52:01
# @Last Modified by:   netrunner-exe
# @Last Modified time: 2022-12-21 17:01:24
import logging

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow_addons.layers import InstanceNormalization

from networks.layers import AdaIN, AdaptiveAttention
from retinaface.models import *
from utils.options import FaceDancerOptions
from utils.swap_func import run_inference

logging.getLogger().setLevel(logging.ERROR)


if __name__ == '__main__':
    opt = FaceDancerOptions().parse()

    if len(tf.config.list_physical_devices('GPU')) != 0:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        tf.config.set_visible_devices(gpus[opt.device_id], 'GPU')

    RetinaFace = load_model(opt.retina_path, compile=False,
                            custom_objects={"FPN": FPN,
                                            "SSH": SSH,
                                            "BboxHead": BboxHead,
                                            "LandmarkHead": LandmarkHead,
                                            "ClassHead": ClassHead})
    ArcFace = load_model(opt.arcface_path, compile=False)

    G = load_model(opt.facedancer_path, compile=False,
                   custom_objects={"AdaIN": AdaIN,
                                   "AdaptiveAttention": AdaptiveAttention,
                                   "InstanceNormalization": InstanceNormalization})
    G.summary()

    run_inference(opt, opt.swap_source, opt.img_path,
                  RetinaFace, ArcFace, G, opt.img_output)
