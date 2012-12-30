//
//  Piece.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Model.h"
#import "PieceType.h"

@class Cell;
@class PieceDecoder;

@interface Piece : Model 
{
	PieceType _pieceType;
	Cell *_cell;
}

@property (nonatomic, readonly) PieceType pieceType;
@property (nonatomic, readwrite, assign) Cell *cell;

+(id) pieceWithPieceType: (PieceType) pieceType andCell: (Cell*) cell;
-(id) initWithPieceType: (PieceType) pieceType andCell: (Cell*) cell;

-(BOOL)isEqualToPiece:(Piece*)otherPiece;

-(void) toEncodedChars: (char[]) chars;
+(PieceDecoder*) pieceDecoderFromEncodedChars: (char[]) chars;

@end

extern NSString *NSStringFromPieceType(PieceType pieceType);









