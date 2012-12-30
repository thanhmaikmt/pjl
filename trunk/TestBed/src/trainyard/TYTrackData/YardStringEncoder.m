//
//  YardStringEncoder.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-04.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "YardStringEncoder.h"
#import "Yard.h"
#import "Cell.h"
#import "Piece.h"
#import "PieceDecoder.h"
#import "EmptyPiece.h"
#import "TrackPiece.h"

static char charList[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_";

@implementation YardStringEncoder

+(NSString*) stringfromYard:(Yard*)yard withPuzzle:(BOOL)shouldEncodePuzzle andWithSolution:(BOOL)shouldEncodeSolution
{
	char yardChars[1024] = "";
	[YardStringEncoder chars:yardChars fromYard:yard withPuzzle:shouldEncodePuzzle andWithSolution:shouldEncodeSolution];

	return [NSString stringWithUTF8String:yardChars];
}


//encode
+(void) chars:(char[])chars fromYard:(Yard*)yard withPuzzle:(BOOL)shouldEncodePuzzle andWithSolution:(BOOL)shouldEncodeSolution
{
	chars[0] = charFromInt(yard.cols);
	chars[1] = charFromInt(yard.rows);
	
	if(shouldEncodePuzzle)
	{
		char puzzleChars[512] = "";
		
		[self puzzleChars:puzzleChars fromYard:yard];
		
		if(strlen(puzzleChars) > 0)
		{
			strcat(chars, puzzleChars);
		}
	}
	
	if(shouldEncodeSolution)
	{
		char solutionChars[512] = "";
		
		[self solutionChars:solutionChars fromYard:yard];
		
		if(strlen(solutionChars) > 0)
		{
			chars[strlen(chars)] = '_';
			strcat(chars, solutionChars);
		}
	}
	
	//NSLog(@"the length is %d and it looks like %s", strlen(chars), chars);
	
	chars[strlen(chars)] = '\0';
}

+(void) puzzleChars:(char[])chars fromYard:(Yard*)yard;
{
	int emptyCount = 0;
	int nonEmptyCount = 0;
	
	int numCells = yard.cols*yard.rows;
	
	char charsToReturn[512] = "";
	
	int charIndex = 0;
	
	for(int c = 0; c<numCells; c++)
	{
		Piece *piece = [yard getCellAtIndex:c].piece;
		
		if(piece.pieceType == PieceType_Track || piece.pieceType == PieceType_Empty)
		{
			emptyCount++;
			if(emptyCount == 10)
			{
				charsToReturn[charIndex++] = '0';
				emptyCount = 0;
			}
		}
		else
		{
			if(emptyCount > 0)
			{
				charsToReturn[charIndex++] = '0'+emptyCount;
				emptyCount = 0;
			}
			
			char pieceChars[16] = "";
			[piece toEncodedChars:pieceChars];
			strcat(charsToReturn, pieceChars);
			charIndex = strlen(charsToReturn);
			nonEmptyCount++;
		}
		
	}
	
	charsToReturn[strlen(charsToReturn)] = '\0';
	
	if(nonEmptyCount > 0) //don't return anything unlesbn there was a real piece here
	{
		strcpy(chars, charsToReturn);
	}
	
	chars[strlen(chars)] = '\0';
}

+(void) solutionChars:(char[])chars fromYard:(Yard*)yard;
{
	int emptyCount = 0;
	int trackCount = 0;
	
	int numCells = yard.cols*yard.rows;
	
	char charsToReturn[512] = "";
	
	int charIndex = 0;
	
	for(int c = 0; c<numCells; c++)
	{
		Piece *piece = [yard getCellAtIndex:c].piece;
		
		if(piece.pieceType == PieceType_Track)
		{
			if(emptyCount > 0)
			{
				charsToReturn[charIndex++] = '0'+emptyCount;
				emptyCount = 0;
			}
			
			char pieceChars[16] = "";
			[piece toEncodedChars:pieceChars];
			strcat(charsToReturn, pieceChars);
			charIndex = strlen(charsToReturn);
			trackCount++;
		}
		else
		{
			emptyCount++;
			if(emptyCount == 10)
			{
				charsToReturn[charIndex++] = '0';
				emptyCount = 0;
			}
		}
	}
	
	if(trackCount > 0) //don't return anything unlesbn there was a real piece here
	{
		strcpy(chars, charsToReturn);
	}
	
	chars[strlen(chars)] = '\0';
}

+(Yard*) yardFromString:(NSString*)string
{
	return [YardStringEncoder yardFromChars:(char*)[string UTF8String]];
}

//decode
+(Yard*) yardFromChars:(char[])chars
{
	int cols = intFromChar(chars[0]);
	int rows = intFromChar(chars[1]);
	int numCells = cols*rows;
	
	NSMutableArray *cells = [NSMutableArray array];
	
	char puzzleChars[512] = "";
	char solutionChars[512] = "";
	
	int splitIndex = getIndexOfCharInChars('_', chars);
	
	if(splitIndex < 0) //it's only a puzzle
	{
		strcat(puzzleChars, chars+2);
	}
	else
	{
		strncat(puzzleChars, chars+2, splitIndex-2);
		strcat(solutionChars, chars+splitIndex+1);
	}
	
	int puzzleLength = strlen(puzzleChars);
	int solutionLength = strlen(solutionChars);
	int puzzleIndex = 0;
	int solutionIndex = 0;
	
	int puzzleEmptyCount = 0;
	int solutionEmptyCount = 0;
	
	
	for(int c = 0; c<numCells; c++)
	{
	
		Piece *piece = nil; 
		
		char puzzleChar = puzzleChars[puzzleIndex];

		//NSLog(@"Round %d %d/%d checking %c", c, puzzleIndex, puzzleLength, puzzleChar);
		
		if(puzzleIndex < puzzleLength && !isdigit(puzzleChar))
		{
			PieceDecoder *decoder =	[PieceDecoder pieceDecoderFromChars:puzzleChars+puzzleIndex];
			puzzleIndex += decoder.numCharsToRemove;
			piece = decoder.piece;
		}
		else
		{
			int charValue = puzzleChar - '0';//get digital value
			
			puzzleEmptyCount++;
			
			if(puzzleEmptyCount == charValue ||
				(puzzleEmptyCount == 10 && charValue == 0))
			{
				puzzleIndex++;
				puzzleEmptyCount = 0;
			}
		}
		
		if(solutionIndex < solutionLength)
		{
			
			
			char solutionChar = solutionChars[solutionIndex];

			if(!isdigit(solutionChar))
			{
				solutionIndex++;
				if(!piece)
				{
					piece = [TrackPiece trackPieceFromChar:solutionChar];
				}
			}
			else
			{
				int charValue = solutionChar - '0';
				
				solutionEmptyCount++;
				
				if(solutionEmptyCount == charValue ||
				   (solutionEmptyCount == 10 && charValue == 0))
				{
					solutionIndex++;
					solutionEmptyCount = 0;
				}
				
				if(!piece)
				{
					piece = [[[EmptyPiece alloc] initWithCell:nil] autorelease];
				}
				
			}
			
		}
		else
		{
			if(!piece)
			{
				piece = [[[EmptyPiece alloc] initWithCell:nil] autorelease];
			}
		}
		
		Cell *cell = [Cell cellWithCol:c%cols andRow:floorf((float)c/cols) andPiece:piece];
		
		[cells addObject:cell];
	}
	
	
	//NSLog(@"PuzzleString %s length:%d", puzzleChars, puzzleLength);
	//NSLog(@"SolutionString %s length:%d", solutionChars, solutionLength);
	
	//NSLog(@"yard has %d,%d  from %c,%c", cols, rows, chars[0], chars[1]);
	
	return [Yard yardWithCols:cols andRows:rows andCells:cells];
}


+(NSString*)getVersion
{
	return @"YardStringEncooder_V01_01";
}

#pragma mark C Functions

char charFromInt(int index)
{
	return charList[index];
}

int intFromChar(char someChar)
{
	char searchString[2] = {someChar, '\0'};
	return (strstr(charList,searchString) - charList);
}

int getIndexOfCharInChars(char searchChar, char *chars)
{
	char searchString[2] = {searchChar, '\0'};
	return (strstr(chars,searchString) - chars);
}

BOOL isCharInChars(char searchChar, char *chars)
{
	return (getIndexOfCharInChars(searchChar, chars) > 0); 
}

@end
