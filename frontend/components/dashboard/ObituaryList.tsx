
import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import ObituaryCard from "@/components/ObituaryCard";
import type { Obituary } from "@/types/obituary";

interface ObituaryListProps {
  obituaries: Obituary[];
  onDelete: (id: string) => Promise<void>;
  onShowCreateForm: () => void;
}

const ObituaryList: React.FC<ObituaryListProps> = ({
  obituaries,
  onDelete,
  onShowCreateForm,
}) => {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Your Obituaries</h3>
      {obituaries.length === 0 ? (
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-muted-foreground mb-4">
              You haven't created any obituaries yet.
            </p>
            <Button onClick={onShowCreateForm}>
              Create Your First Obituary
            </Button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2">
          {obituaries.map((obituary) => (
            <ObituaryCard
              key={obituary.id}
              obituary={obituary}
              onDelete={onDelete}
              showActions={true}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default ObituaryList;
