"use client"

import { useState } from "react"
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"

interface ExportModalProps {
  isOpen: boolean
  onClose: () => void
}

export function ExportModal({ isOpen, onClose }: ExportModalProps) {
  const [platform, setPlatform] = useState<string>("all")
  const [category, setCategory] = useState<string>("")
  const [product, setProduct] = useState<string>("")

  const handleExport = () => {
    console.log("[v0] Export data:", { platform, category, product })
    onClose()
  }

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Export Data</DialogTitle>
          <DialogDescription>Select data to export (Maximum 2 weeks of data available).</DialogDescription>
        </DialogHeader>

        <div className="space-y-6 py-4">
          <div className="space-y-3">
            <Label>Platform</Label>
            <RadioGroup value={platform} onValueChange={setPlatform}>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="all" id="all" />
                <Label htmlFor="all" className="font-normal">
                  All
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="@cosme" id="cosme" />
                <Label htmlFor="cosme" className="font-normal">
                  @cosme
                </Label>
              </div>
              <div className="flex items-center space-x-2">
                <RadioGroupItem value="Amazon" id="amazon" />
                <Label htmlFor="amazon" className="font-normal">
                  Amazon
                </Label>
              </div>
            </RadioGroup>
          </div>

          <div className="space-y-2">
            <Label>Category</Label>
            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="skincare">Skincare</SelectItem>
                <SelectItem value="makeup">Makeup</SelectItem>
                <SelectItem value="bodycare">Body Care</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label>Product Name</Label>
            <Select value={product} onValueChange={setProduct} disabled={!category}>
              <SelectTrigger>
                <SelectValue placeholder="Select product" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="product1">Laneige Water Sleeping Mask</SelectItem>
                <SelectItem value="product2">Laneige Lip Sleeping Mask</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="flex justify-end gap-3">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button onClick={handleExport}>Export</Button>
        </div>
      </DialogContent>
    </Dialog>
  )
}
