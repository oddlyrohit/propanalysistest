import { Badge } from "@/components/ui/badge"
import { GraduationCap, Users, TrendingUp } from "lucide-react"
import type { School } from "@/types"

interface SchoolsListProps {
  schools?: School[]
}

export function SchoolsList({ schools }: SchoolsListProps) {
  if (!schools || schools.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <GraduationCap className="h-12 w-12 mx-auto mb-2 opacity-50" />
        <p>No school data available</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {schools.map((school, index) => (
        <div
          key={index}
          className="p-4 rounded-lg border border-border bg-card hover:bg-accent/50 transition-colors"
        >
          {/* School Name and Type */}
          <div className="flex items-start justify-between mb-3">
            <div className="flex items-start gap-3 flex-1">
              <div className="p-2 rounded-lg bg-primary/10">
                <GraduationCap className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1">
                <h4 className="font-semibold text-foreground">{school.name}</h4>
                <div className="flex items-center gap-2 mt-1 flex-wrap">
                  <Badge variant="secondary" className="text-xs">
                    {school.type}
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    {school.sector}
                  </Badge>
                  {school.distance !== undefined && (
                    <span className="text-xs text-muted-foreground">{school.distance.toFixed(1)}km away</span>
                  )}
                </div>
              </div>
            </div>

            {/* Rating Display */}
            {school.rating !== undefined && (
              <div className="text-right ml-4">
                <div className="text-sm font-semibold text-foreground">{school.rating.toFixed(1)}/5.0</div>
                <div className="text-xs text-muted-foreground">Rating</div>
              </div>
            )}
          </div>

          {/* Additional Real API Data */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3 pt-3 border-t border-border">
            {/* NAPLAN Score */}
            {school.naplanRank && (
              <div className="flex items-center gap-2 text-sm">
                <TrendingUp className="h-4 w-4 text-green-600" />
                <div>
                  <div className="font-medium text-foreground">{school.naplanRank}</div>
                  <div className="text-xs text-muted-foreground">Academic Performance</div>
                </div>
              </div>
            )}

            {/* Student Count */}
            {school.students && (
              <div className="flex items-center gap-2 text-sm">
                <Users className="h-4 w-4 text-blue-600" />
                <div>
                  <div className="font-medium text-foreground">
                    {school.students.total} students
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {school.students.boys} boys, {school.students.girls} girls
                  </div>
                </div>
              </div>
            )}

            {/* Attendance Rate */}
            {school.attendanceRate && (
              <div className="flex items-center gap-2 text-sm">
                <div className="h-4 w-4 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                  <div className="h-2 w-2 rounded-full bg-green-600"></div>
                </div>
                <div>
                  <div className="font-medium text-foreground">
                    {(school.attendanceRate * 100).toFixed(0)}% attendance
                  </div>
                  <div className="text-xs text-muted-foreground">Attendance rate</div>
                </div>
              </div>
            )}
          </div>

          {/* Socioeconomic Rank */}
          {school.socioeconomicRank && (
            <div className="mt-2 pt-2 border-t border-border">
              <div className="text-xs text-muted-foreground">
                {school.socioeconomicRank}
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  )
}

