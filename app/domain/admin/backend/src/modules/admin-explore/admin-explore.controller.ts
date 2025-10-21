import { Controller, Get, Patch, Param, Body, UseGuards } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse, ApiBearerAuth } from '@nestjs/swagger';
import { AdminExploreService } from './admin-explore.service';
import { JwtAuthGuard } from '../auth/guards/jwt-auth.guard';

@ApiTags('Admin Explore')
@Controller('admin')
@UseGuards(JwtAuthGuard)
@ApiBearerAuth()
export class AdminExploreController {
  constructor(private readonly adminExploreService: AdminExploreService) {}

  @Get('dashboard')
  @ApiOperation({ summary: 'Get dashboard statistics' })
  @ApiResponse({ status: 200, description: 'Dashboard stats retrieved successfully' })
  async getDashboardStats() {
    return this.adminExploreService.getDashboardStats();
  }

  @Get('tables')
  @ApiOperation({ summary: 'Get all tables' })
  @ApiResponse({ status: 200, description: 'Tables retrieved successfully' })
  async getAllTables() {
    return this.adminExploreService.getAllTables();
  }

  @Get('tables/:formId')
  @ApiOperation({ summary: 'Get table details' })
  @ApiResponse({ status: 200, description: 'Table details retrieved successfully' })
  @ApiResponse({ status: 404, description: 'Table not found' })
  async getTableDetails(@Param('formId') formId: string) {
    return this.adminExploreService.getTableDetails(formId);
  }

  @Patch('tables/:formId/settings')
  @ApiOperation({ summary: 'Update table settings' })
  @ApiResponse({ status: 200, description: 'Table settings updated successfully' })
  async updateTableSettings(@Param('formId') formId: string, @Body() settings: any) {
    return this.adminExploreService.updateTableSettings(formId, settings);
  }

  @Get('activity')
  @ApiOperation({ summary: 'Get recent activity' })
  @ApiResponse({ status: 200, description: 'Recent activity retrieved successfully' })
  async getRecentActivity() {
    return this.adminExploreService.getRecentActivity();
  }
}


