//
//  YardStringEncoder.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-04.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

@class Yard;

@interface YardStringEncoder : NSObject 
{

}

+(NSString*) stringfromYard:(Yard*)yard withPuzzle:(BOOL)shouldEncodePuzzle andWithSolution:(BOOL)shouldEncodeSolution;

+(void) chars:(char[])chars fromYard:(Yard*)yard withPuzzle:(BOOL)shouldEncodePuzzle andWithSolution:(BOOL)shouldEncodeSolution;
+(void) puzzleChars:(char[])chars fromYard:(Yard*)yard;
+(void) solutionChars:(char[])chars fromYard:(Yard*)yard;

+(Yard*) yardFromString:(NSString*)string;

+(Yard*) yardFromChars:(char[])chars;


#pragma mark C Functions
char charFromInt(int index);
int intFromChar(char someChar);
int getIndexOfCharInChars(char searchChar, char *chars);
BOOL isCharInChars(char searchChar, char *chars);
BOOL isCharNumeric(char someChar);

+(NSString*)getVersion;

@end
