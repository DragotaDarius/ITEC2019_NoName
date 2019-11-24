#!/bin/sh
echo "ab1"
cd ~/open_model_zoo/demos/build/armv7l/Release
./interactive_face_detection_demo -d HETERO:MYRIAD -i "cam" HETERO:MYRIAD -m ~/interactive_face_detection_demo/face-detection-retail-0004.xml -d_ag HETERO:MYRIAD -m_ag ~/interactive_face_detection_demo/age-gender-recognition-retail-0013.xml -d_em HETERO:MYRIAD -m_em ~/interactive_face_detection_demo/emotions-recognition-retail-0003.xml -d_hp HETERO:MYRIAD -m_hp ~/interactive_face_detection_demo/head-pose-estimation-adas-0001.xml -r 
echo "ab2"
