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
		moorePoint = currentCell + Point{-1, 1};
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
		moorePoint = currentCell + Point{ 1,-1 };
		break;
	}
	case(5): {
		step = { 1, 1 };
		moorePoint = currentCell + Point{ 1,0 };
		break;
	}
	case(6): {
		step = { 0, 1 };
		moorePoint = currentCell + Point{ 1,1 };
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
	if (stepDifference == Point{ -1, 0 }) { //the location of c0 in perspective of the currentCell b0
		mooreNr = 0;
		
	}
	else if (stepDifference == Point{ -1, -1 }) {
		mooreNr = 1;
		
	}
	else if (stepDifference == Point{ 0, -1 }) {
		mooreNr = 2;
		
	}
	else if (stepDifference == Point{ 1, -1 }) {
		mooreNr = 3;
		
	}
	else if (stepDifference == Point{ 1, 0 }) {
		mooreNr = 4;
		
	}
	else if (stepDifference == Point{ 1, 1 }) {
		mooreNr = 5;
		
	}
	else if (stepDifference == Point{ 0, 1 }) {
		mooreNr = 6;
		
	}
	else if (stepDifference == Point{ -1, 1 }) {
		mooreNr = 7;
	
	}


	return mooreNr;
}


Point clockwise(Point &currentCell, Mat binaryImage, Point &moorePoint) {
	//determine mooreNr 
	
	int mooreNr = determineMooreNr(moorePoint, currentCell);
	
	Point coordinateB;
	
	int mooreIteration{ 0 };
	for (mooreIteration; mooreIteration < 8; mooreIteration++) {
		
		Point step = determinePath(mooreNr + mooreIteration, moorePoint, currentCell);

		coordinateB = currentCell + step;
		if (coordinateB == Point(209,108)) {
			cout << "Hiero" << endl;
		}
		if (binaryImage.at<__int16>(coordinateB) == 1) {
			
			return coordinateB;
			break;
			
		}
	}

	return -1;
}



int allContours(Mat binaryImage, vector<vector<Point>> &contours) {
	// Find number of BLOBs to determine number of rows in matrix contours
	int numBlobs = labelBLOBs(binaryImage, binaryImage);

	// For each blob, determine contour coordinates
	for (int N = 0; N < numBlobs; N++) 
	{
		vector<Point> rowContours;

		// find first cell where the moore algorithm needs to start
		Point firstCell;
		bool firstFound{ false };
		Point currentCell;
		int row{ 0 }; // row and col are indices 
		for (row; row < binaryImage.rows; row++)
		{
			int col{ 0 };
			for (col; col < binaryImage.cols; col++)
			{
				if (binaryImage.at<__int16>(row, col) != 0) // when first pixel is found, save in contours
				{
					firstCell = Point{ col,row };
					//currentCell = firstCell;
					rowContours.push_back(firstCell);
					firstFound = true;
					break;
				}
			}
			if (firstFound) //break loops if first pixel is found
			{
				break;
			}
		}
		// find contourpixel per iteration
		int ii{ 0 };
		Point moorePoint = firstCell + Point(-1,0);
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



