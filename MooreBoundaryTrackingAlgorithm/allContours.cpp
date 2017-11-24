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

Point determinePath(int mooreIteration, Point &moorePoint, Point currentCell) {
	//determine path 
	Point step;
	int mooreNr = mooreIteration % 8;
	switch (mooreNr) {//steps the object needs to make
		case(0): {
			step = { -1, 0 };
			moorePoint = currentCell + Point{ -1, 1 };
			break;
		}
		case(1): {
			step = { -1,-1 };
			moorePoint = currentCell + Point{ -1, 0 };
			break;
		}
		case(2): {
			step = { 0,-1 };
			moorePoint = currentCell + Point{ -1,-1 };
			break;
		}
		case(3): {
			step = { 1,-1 };
			moorePoint = currentCell + Point{ 0,-1 };
			break;
		}
		case(4): {
			step = { 1, 0 };
			moorePoint = currentCell + Point{ 1, -1 };
			break;
		}
		case(5): {
			step = { 1, 1 };
			moorePoint = currentCell + Point{ 1, 0 };
			break;
		}
		case(6): {
			step = { 0, 1 };
			moorePoint = currentCell + Point{ 1, 1 };
			break;
		}
		case(7): {
			step = { -1, 1 };
			moorePoint = currentCell + Point{ 0,1 };
			break;
		}
	};
	return step;
}

int determineMooreNr(Point moorePoint, Point currentCell) {
	// determine mooreNr aka determining the iteration point for determinePath
	Point stepDifference = moorePoint - currentCell;
	int mooreNr{ -1 };
	//the location of c0 in perspective of the currentCell b0
	if (stepDifference == Point{ -1, 0 })		mooreNr = 0;
	else if (stepDifference == Point{ -1, -1 }) mooreNr = 1;
	else if (stepDifference == Point{ 0, -1 })  mooreNr = 2;
	else if (stepDifference == Point{ 1, -1 })  mooreNr = 3;
	else if (stepDifference == Point{ 1, 0 })	mooreNr = 4;
	else if (stepDifference == Point{ 1, 1 }) 	mooreNr = 5;
	else if (stepDifference == Point{ 0, 1 }) 	mooreNr = 6;
	else if (stepDifference == Point{ -1, 1 }) 	mooreNr = 7;

	return mooreNr;
}

Point clockwise(Point &currentCell, Mat binaryImage, Point &moorePoint) {
	//determine mooreNr 
	int mooreNr = determineMooreNr(moorePoint, currentCell);
	
	Point coordinate; //This object walks around the currentcell to find the neighbour
	int mooreIteration{ 0 };
	for (mooreIteration; mooreIteration < 8; mooreIteration++) {
		
		Point step = determinePath(mooreNr + mooreIteration, moorePoint, currentCell);
		coordinate = currentCell + step;
		
		if (coordinate == Point(6, 6)) {
			cout << binaryImage.at<__int16>(coordinate) << endl;
		}
		
		if (binaryImage.at<__int16>(coordinate) >= 1) {
			return coordinate;
			break;	
		}
	}

	return -1;
}

int allContours(Mat binaryImage, vector<vector<Point>> &contours) {
	// Find number of BLOBs to determine number of rows in matrix contours
	vector<Point2d*> firstPixelVec;
	vector<Point2d*> posVec;
	vector<int> areaVec;

	int numBlobs = labelBLOBsInfo(binaryImage, binaryImage, firstPixelVec, posVec, areaVec, 1, INT_MAX); //int numBlobs = labelBLOBs(binaryImage, binaryImage);

	// For each blob, determine contour coordinates
	for (int N = 0; N < numBlobs; N++) 
	{
		vector<Point> rowContours;

		int firstCellrow = firstPixelVec[N]->x;
		int firstCellcol = firstPixelVec[N]->y;
		Point firstCell = { firstCellcol, firstCellrow };
		Point currentCell;


		// find contourpixel per iteration
		int ii{ 0 };
		Point moorePoint = firstCell + Point(-1,0);
		rowContours.push_back(firstCell);

		while(currentCell != firstCell ) {
			if (ii == 0) {
				currentCell = firstCell;
			}
			currentCell = clockwise(currentCell, binaryImage, moorePoint);
			rowContours.push_back(currentCell);
			ii++;
		}
		contours.push_back(rowContours);
		rowContours.clear();	
	}
	return numBlobs;
}