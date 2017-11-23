#pragma once

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv/cv.h>
#include <iostream>
#include <string>
#include <vector>
#include "avansvisionlib\avansvisionlib.h"

using namespace cv;
using namespace std;

Point determinePath(int mooreIteration, Point &moorePoint, Point currentCell);
int determineMooreNr(Point moorePoint, Point currentCell);
Point clockwise(Point &currentCell, Mat binaryImage, Point &moorePoint);
int allContours(Mat binaryImage, vector<vector<Point>> &contours);