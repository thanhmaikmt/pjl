//
//  EmptyPiece.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Piece.h"

@class Cell;

@interface EmptyPiece : Piece 
{

}

- (id)initWithCell: (Cell*) cell;

- (void) undo;

@end

@protocol EmptyPieceDelegate <NSObject>

-(void)onUndo;

@end
