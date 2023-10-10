:: Avoid printing all the comments in the Windows cmd
@echo off

echo ------------------------- BODY, FOOT, FACE, AND HAND MODELS -------------------------
echo ----- Downloading body pose (COCO and MPI), face and hand models -----
SET WGET_EXE=openpose\3rdparty\windows\wget\wget.exe
SET OPENPOSE_URL=http://posefs1.perception.cs.cmu.edu/OpenPose/models/
SET POSE_FOLDER=pose/
SET FACE_FOLDER=face/
SET HAND_FOLDER=hand/

:: Create the folders if they don't exist
IF NOT EXIST %POSE_FOLDER% mkdir %POSE_FOLDER%

IF NOT EXIST %FACE_FOLDER% mkdir %FACE_FOLDER%

IF NOT EXIST %HAND_FOLDER% mkdir %HAND_FOLDER%



echo:
echo ------------------------- POSE (BODY+FOOT) MODELS -------------------------
echo Body (BODY_25)
set BODY_25_FOLDER=%POSE_FOLDER%body_25/
IF NOT EXIST %BODY_25_FOLDER% mkdir %BODY_25_FOLDER%
set BODY_25_MODEL=%BODY_25_FOLDER%pose_iter_584000.caffemodel
echo  %OPENPOSE_URL%%BODY_25_MODEL%
%WGET_EXE% -c %OPENPOSE_URL%%BODY_25_MODEL% -P %BODY_25_FOLDER%
echo ----------------------- POSE DOWNLOADED -----------------------

echo:
echo ------------------------- FACE MODELS -------------------------
echo Face
SET FACE_MODEL=%FACE_FOLDER%pose_iter_116000.caffemodel
echo  %OPENPOSE_URL%%FACE_MODEL%

%WGET_EXE% -c %OPENPOSE_URL%%FACE_MODEL% -P %FACE_FOLDER%
echo ----------------------- FACE DOWNLOADED -----------------------

echo:
echo ------------------------- HAND MODELS -------------------------
echo Hand
SET HAND_MODEL=%HAND_FOLDER%pose_iter_102000.caffemodel
echo  %OPENPOSE_URL%%HAND_MODEL%

%WGET_EXE% -c %OPENPOSE_URL%%HAND_MODEL% -P %HAND_FOLDER%
echo ----------------------- HAND DOWNLOADED -----------------------
