//
//  PieceDecoder.m
//  Trainyard
//
//  Created by Matt Rix on 09-10-04.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import "PieceDecoder.h"
#import "RockPiece.h"
#import "OutletPiece.h"
#import "EmptyPiece.h"
#import "PainterPiece.h"
#import "GoalPiece.h"
#import "SplitterPiece.h"

@implementation PieceDecoder

@synthesize piece = _piece;
@synthesize numCharsToRemove = _numCharsToRemove;

+(id) pieceDecoderFromChars:(char[])chars
{
	//NSLog(@"Checking char %c", chars[0]);
	switch(chars[0])
	{
		case 'R': return [RockPiece pieceDecoderFromEncodedChars:chars];
		case 'O': return [OutletPiece pieceDecoderFromEncodedChars:chars];		
		case 'P': return [PainterPiece pieceDecoderFromEncodedChars:chars];	
		case 'G': return [GoalPiece pieceDecoderFromEncodedChars:chars];
		case 'S': return [SplitterPiece pieceDecoderFromEncodedChars:chars];	
	}
	
	//NSLog(@"Decoder char wasn't found, so returing piece");
	return [EmptyPiece pieceDecoderFromEncodedChars:chars];
}

+(id) pieceDecoderWithPiece:(Piece*)piece andNumCharsToRemove:(int)numCharsToRemove
{
	return [[[PieceDecoder alloc] initWithPiece:piece andNumCharsToRemove:numCharsToRemove] autorelease];
}

-(id) initWithPiece:(Piece*)piece andNumCharsToRemove:(int)numCharsToRemove
{
	self = [super init];
	if(self)
	{
		_piece = [piece retain];
		_numCharsToRemove = numCharsToRemove;
	}
	return self;
}

-(void) dealloc
{
	[_piece release];
	[super dealloc];
}

@end
