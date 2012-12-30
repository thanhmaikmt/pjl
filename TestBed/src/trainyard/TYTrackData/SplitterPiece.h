//
//  SplitterPiece.h
//  Trainyard
//
//  Created by Matt Rix on 09-10-03.
//  Copyright 2009 __MyCompanyName__. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "Piece.h"
#import "DestinationPieceProtocol.h"
#import "CreatorPieceProtocol.h"

@class Cell;
@class TYSide;

@interface SplitterPiece : Piece <DestinationPieceProtocol, CreatorPieceProtocol>
{
	TYSide *_sideIn;
	TYSide *_sideOutLeft;
	TYSide *_sideOutRight;	
	NSMutableArray *_trainsToCreate;
}

@property (nonatomic, readwrite, assign) TYSide *sideIn;

- (id)initWithSideIn:(TYSide*)sideIn andCell:(Cell*)cell;;
-(void) updateSidesOut;

@end

@protocol SplitterPieceDelegate <NSObject>

-(void)onSplit;

@end

