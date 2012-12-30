//
//  PieceDecoder.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-04.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>

@class Piece;

@interface PieceDecoder : NSObject 
{
	Piece *_piece;
	int _numCharsToRemove;
}

@property (nonatomic, readonly) Piece *piece;
@property (nonatomic, readonly) int numCharsToRemove;

+(id) pieceDecoderFromChars:(char[])chars;
+(id) pieceDecoderWithPiece:(Piece*)piece andNumCharsToRemove:(int)numCharsToRemove;
-(id) initWithPiece:(Piece*)piece andNumCharsToRemove:(int)numCharsToRemove;

@end
