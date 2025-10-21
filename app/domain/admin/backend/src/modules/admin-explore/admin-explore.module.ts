import { Module } from '@nestjs/common';
import { AdminExploreController } from './admin-explore.controller';
import { AdminExploreService } from './admin-explore.service';

@Module({
  controllers: [AdminExploreController],
  providers: [AdminExploreService],
  exports: [AdminExploreService],
})
export class AdminExploreModule {}


